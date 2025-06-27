from zipfile import ZipFile
from xml.etree.ElementTree import ParseError
from flask import Blueprint, request, jsonify
from utils.tools import get_config
from schema.documentos import Documento
from lib.evschema import DBConfig
from utils.db import _mysql_errors, mysql
from datetime import datetime

doc_router = Blueprint(
    "documentos_fiscales_route", __name__, url_prefix="documentos"
)


def camel_to_snake_better(name):
    import re

    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return name.lower()


@doc_router.errorhandler(ValueError)
def handle_value_error(e: ValueError):
    return jsonify({"error": True, "message": e.args[0], "status_code": 400})


@doc_router.route("/")
def doc_search():
    try:

        data = mysql.search(model="documentos", **request.args)

        return {
            "error": False,
            "data": data.get("result", []),
            "total_rows": data.get("total_rows", 0),
        }
    except _mysql_errors.ProgrammingError as e:
        raise ValueError(e.args)


@doc_router.route("/<rfc>")
def doc_rfc_documentos(rfc: str):

    fields = request.args.get("fields", "*")
    limit = request.args.get("limit", 50)
    startdate = request.args.get("startdate", None)
    enddate = request.args.get("enddate", None)

    wheres = ""

    if startdate is not None and enddate is not None:
        wheres = f"AND fecha BETWEEN '{startdate}' AND '{enddate}'"

    query = f"SELECT {fields} FROM documentos WHERE receptor_rfc='{rfc}' {wheres} LIMIT {limit}"
    documentos_recibidos = mysql.fetchall(query)
    if documentos_recibidos is None:
        documentos_recibidos = []

    query = f"SELECT {fields} FROM documentos WHERE emisor_rfc='{rfc}' {wheres} LIMIT {limit}"
    documentos_emitidos = mysql.fetchall(query)
    if documentos_emitidos is None:
        documentos_emitidos = []

    query = f"SELECT razon_social, rfc FROM clients WHERE rfc='{rfc}'"

    query = f"""
    SELECT
        c.id,c.razon_social,c.rfc,c.email,
        mp.codigo metodo_pago_codigo,
        mp.descripcion metodo_pago,
        rf.codigo regimen_fiscal_codigo,
        rf.descripcion regimen_fiscal
        FROM clients c, metodo_pago mp,regimenes_fiscales rf 
        WHERE rfc='{rfc}' AND mp.id=c.metodo_pago_id AND rf.id=c.regimen_fiscal_id;
    """
    client = mysql.fetchone(query)
    if client is None:
        client = {}

    return {
        "error": False,
        "data": {
            "documentos_recibidos": documentos_recibidos,
            "documentos_emitidos": documentos_emitidos,
            "client": client,
        },
    }


@doc_router.route("/save", methods=["POST"])
def doc_fis_save():

    def document_worker(xml_content: str) -> int:

        xml_content = xml_content.replace("'", "")
        try:
            from lib.comprobante_fiscal_sat import ComprobanteFiscal

            cf = ComprobanteFiscal.convertirxml(xml_content)

            if cf is not None:
                config = DBConfig(**get_config()["mysql"])
                doc = Documento(config=config)

                doc.receptor = cf.receptor.Nombre
                doc.receptor_rfc = cf.receptor.Rfc
                doc.emisor = cf.emisor.Nombre
                doc.emisor_rfc = cf.emisor.Rfc
                doc.version = cf.comprobante.Version
                doc.serie = cf.comprobante.Serie
                doc.folio = cf.comprobante.Folio
                doc.fecha = cf.comprobante.Fecha
                doc.sello = cf.comprobante.Sello
                doc.forma_pago = cf.comprobante.FormaPago
                doc.nocertificado = cf.comprobante.NoCertificado
                doc.moneda = cf.comprobante.Moneda
                doc.tipo_cambio = cf.comprobante.TipoCambio
                doc.subtotal = cf.comprobante.SubTotal
                doc.total = cf.comprobante.Total
                doc.tipo_de_comprobante = cf.comprobante.TipoDeComprobante
                doc.exportacion = cf.comprobante.Exportacion
                doc.metodo_pago = cf.comprobante.MetodoPago
                doc.uuid_comprobante = cf.timbrefiscal.UUID
                doc.fecha_timbrado = cf.timbrefiscal.FechaTimbrado
                doc.impuestos_retenidos = cf.comprobante.TotalImpuestosRetenidos
                doc.impuestos_trasladados = cf.comprobante.TotalImpuestosTrasladados
                doc.xml = xml_content

                result = doc.save()
                if not result.error:

                    query = """
                        INSERT INTO documento_conceptos
                        (documento_id,valor_unitario,objeto_impuesto,noidentificacion,
                        importe,descripcion,clave_prodserv,cantidad) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s)
                    """

                    for concepto in cf.conceptos:
                        args = (
                            result.id,
                            concepto.ValorUnitario,
                            concepto.ObjetoImp,
                            concepto.NoIdentificacion,
                            concepto.Importe,
                            concepto.Descripcion,
                            concepto.ClaveProdServ,
                            concepto.Cantidad,
                        )

                        concepto_id = mysql.commit(query, args)

                        args = []

                        for impuesto in concepto.Impuestos:
                            args.append(
                                (
                                    result.id,
                                    concepto_id.get("lastrowid", 0),
                                    impuesto.tipo,
                                    impuesto.TipoFactor,
                                    impuesto.TasaOCuota,
                                    impuesto.Impuesto,
                                    impuesto.Importe,
                                    impuesto.Base,
                                )
                            )

                        query = """
                            INSERT INTO documento_impuestos
                            (documento_id,concepto_id,tipo_impuesto,
                            tipo_factor,tasa_o_couta,impuesto,importe,base) VALUES
                            (%s,%s,%s,%s,%s,%s,%s,%s)
                        """
                        mysql.executemany(query=query, args=args)

                    return result.id
                else:
                    return None
            else:
                return None

        except _mysql_errors.ProgrammingError as e:
            raise ValueError(e.args)
        except ParseError as e:
            raise ValueError(e.args)
        except ValueError as e:
            raise ValueError(e.args)

    if request.files:

        for file in request.files:
            file = request.files[file]

            inserted_ids = []
            total_docs = 0

            if file.content_type == "application/x-zip-compressed":
                with ZipFile(file, "r") as zipfile:
                    for filename in zipfile.namelist():
                        if filename.endswith(".xml"):
                            with zipfile.open(filename, "r") as xmlfile:
                                _id = document_worker(xmlfile.read().decode("utf-8"))
                                if _id is not None:
                                    inserted_ids.append(_id)
                                    total_docs += 1

                return {"error": False, "data": inserted_ids}

            elif file.content_type == "text/xml":
                _id = document_worker(file.stream.read().decode("utf-8"))
                inserted_ids.append(_id)
                total_docs = 1

            else:
                raise ValueError("No es un archivo valido.")

        return {
            "error": False,
            "message": "Cargado exitoso",
            "ids": inserted_ids,
            "total_documents": total_docs,
        }
    else:
        raise ValueError("Debe de cargar un archivo.")

@doc_router.route('/reportes/impuestos')
def doc_impuestos():

    impuestos = {}
    def works(tipo: str):

        field_rfc = 'emisor_rfc'

        if tipo == 'recibidos': field_rfc = 'receptor_rfc'

        query = """
            SELECT * FROM documentos WHERE {}='VAME890407PG8' AND tipo_de_comprobante="I";
        """.format(field_rfc)
        
        records = mysql.fetchall(query)
        impuestos[tipo] = records
    
    works('emitidos')
    works('recibidos')

    return impuestos