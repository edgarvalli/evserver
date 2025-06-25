from zipfile import ZipFile
from xml.etree.ElementTree import ParseError
from flask import Blueprint, request, jsonify
from utils.tools import get_config
from schema.documentosfiscales import DocumentoFiscal
from lib.evschema import DBConfig
from utils.db import _mysql_errors, mysql

doc_route = Blueprint(
    "documentos_fiscales_route", __name__, url_prefix="documentos_fiscales"
)


def camel_to_snake_better(name):
    import re

    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return name.lower()


@doc_route.errorhandler(ValueError)
def handle_value_error(e: ValueError):
    return jsonify({"error": True, "message": e.args[0], "status_code": 400})


@doc_route.route("/")
def doc_search():
    try:
        return {"error": False, "data": mysql.search(model='documentos_fiscales', **request.args)}
    except _mysql_errors.ProgrammingError as e:
        raise ValueError(e.args)


@doc_route.route("/save", methods=["POST"])
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
            print(xml_content)
            raise ValueError(e.args)

    if request.files:

        for file in request.files:
            file = request.files[file]

            if file.content_type == "application/x-zip-compressed":
                inserted_ids = []
                with ZipFile(file, "r") as zipfile:
                    for filename in zipfile.namelist():
                        if filename.endswith(".xml"):
                            with zipfile.open(filename, "r") as xmlfile:
                                _id = document_worker(xmlfile.read().decode("utf-8"))
                                if _id is not None:
                                    inserted_ids.append(_id)

                return {"error": False, "data": inserted_ids}

            elif file.content_type == "text/xml":
                document_worker(file.stream.read().decode("utf-8"))
            else:
                raise ValueError("No es un archivo valido.")

        return {"error": False, "message": "Cargado exitoso"}
    else:
        raise ValueError("Debe de cargar un archivo.")
