from zipfile import ZipFile
from xml.etree.ElementTree import ParseError
from flask import Blueprint, request, jsonify
from utils.tools import get_config
from schema.documentosfiscales import DocumentoFiscal
from lib.evschema import DBConfig
from utils.db import _mysql_errors, mysql
from datetime import datetime

doc_router = Blueprint(
    "documentos_fiscales_route", __name__, url_prefix="documentos_fiscales"
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

        data = mysql.search(model="documentos_fiscales", **request.args)

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

    query = f"SELECT {fields} FROM documentos_fiscales WHERE receptor_rfc='{rfc}' {wheres} LIMIT {limit}"
    documentos_recibidos = mysql.fetchall(query)
    if documentos_recibidos is None:
        documentos_recibidos = []

    query = f"SELECT {fields} FROM documentos_fiscales WHERE emisor_rfc='{rfc}' {wheres} LIMIT {limit}"
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
                df = DocumentoFiscal(config=config)

                df.receptor = cf.receptor.Nombre
                df.receptor_rfc = cf.receptor.Rfc
                df.emisor = cf.emisor.Nombre
                df.emisor_rfc = cf.emisor.Rfc
                df.version = cf.comprobante.Version
                df.serie = cf.comprobante.Serie
                df.folio = cf.comprobante.Folio
                df.fecha = cf.comprobante.Fecha
                df.sello = cf.comprobante.Sello
                df.forma_pago = cf.comprobante.FormaPago
                df.nocertificado = cf.comprobante.NoCertificado
                df.moneda = cf.comprobante.Moneda
                df.tipo_cambio = cf.comprobante.TipoCambio
                df.subtotal = cf.comprobante.SubTotal
                df.total = cf.comprobante.Total
                df.tipo_de_comprobante = cf.comprobante.TipoDeComprobante
                df.exportacion = cf.comprobante.Exportacion
                df.metodo_pago = cf.comprobante.MetodoPago
                df.uuid_comprobante = cf.timbrefiscal.UUID
                df.fecha_timbrado = cf.timbrefiscal.FechaTimbrado
                df.xml = xml_content

                result = df.save()
                if not result.error:

                    query = """
                        INSERT INTO documentos_fiscales_conceptos
                        (documento_fiscal_id,valor_unitario,objeto_impuesto,noidentificacion,
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
                            INSERT INTO documentos_fiscales_impuestos
                            (documento_fiscal_id,documento_fiscal_concepto_id,tipo_impuesto,
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

@doc_router.route('/reports/impuestos')
def doc_impuestos():

    impuestos = {}
    def works(tipo: str):

        field_rfc = 'emisor_rfc'

        if tipo == 'recibidos': field_rfc = 'receptor_rfc'

        query = """
            SELECT
                impuesto.id, impuesto.importe, df.uuid_comprobante,impuesto.tipo_impuesto,
                impuesto.impuesto, df.serie, df.fecha_timbrado
            FROM documentos_fiscales_impuestos impuesto, documentos_fiscales df
            WHERE impuesto.documento_fiscal_id=df.id
            AND df.fecha_timbrado BETWEEN '2024-01-01' AND '2024-12-31'
            AND df.{} = 'VAME890407PG8';
        """.format(field_rfc)
        
        records = mysql.fetchall(query)

        for doc in records:
            
            fecha: datetime = doc['fecha_timbrado']
            index = fecha.month

            if not index in impuestos: impuestos[index] = {}
            if not tipo in impuestos[index]: impuestos[index][tipo] = {}

            key = str(doc['tipo_impuesto']).lower()
            print(key)
    
    works('emitidos')
    works('recibidos')

    return impuestos