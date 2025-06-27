from lib.evschema import models, columns


class Documento(models.Model):
    _name = "documentos"
    _description = "Tabla donde se guardan todos los CFDIs"

    emisor = columns.Char("Emisor", size=200)
    emisor_rfc = columns.Char("RFC Emisor", size=13)
    receptor = columns.Char("Emisor", size=200)
    receptor_rfc = columns.Char("RFC Emisor", size=13)
    version = columns.Char("Version", size=10)
    serie = columns.Char("Serie", size=50)
    folio = columns.Char("Folio", size=50)
    fecha = columns.DateTime("Fecha")
    sello = columns.Text("Sello")
    forma_pago = columns.Char("Forma de pago")
    nocertificado = columns.Char("No. Certificado")
    certificado = columns.Text("Certificado")
    moneda = columns.Char("Moneda", size=10)
    tipo_cambio = columns.Float("Tipo de Cambio")
    subtotal = columns.Float("Subtotal")
    total = columns.Float("Total")
    tipo_de_comprobante = columns.Char("Tipo de Comprobante", size=4)
    exportacion = columns.Char("Exportacion")
    metodo_pago = columns.Char("Metodo de pago")
    uuid_comprobante = columns.Char('UUID', size=100, unique=True, index=True)
    fecha_timbrado = columns.DateTime('Fecha de Timbrado')
    impuestos_retenidos = columns.Float('Impuestos Retenidos', default=0)
    impuestos_trasladados = columns.Float('Impuestos Trasladados', default=0)
    estatus_pago = columns.Integer("Estado de Pago") # 0 - No pagado, 1 - Pagado, 2 - Pagado Parcial
    xml = columns.Text('XML')


class DocumentoConceptos(models.Model):
    _name = "documento_conceptos"
    _description = "Tabla de conceptos de los documentos"

    documento_id = columns.Integer("ID Documento Fiscal")
    clave_prodserv = columns.Char('Clave Producto o Servicio')
    noidentificacion = columns.Char('No. Identificacion')
    cantidad = columns.Float('Cantidad')
    descripcion = columns.Char('Descripcion', size=300)
    valor_unitario = columns.Float('Valor Unitario')
    importe = columns.Float('Importe')
    objeto_impuesto = columns.Char('Objeto de Impuesto')

class DocumentoImpuestos(models.Model):
    _name = 'documento_impuestos'


    documento_id = columns.Integer('ID Documento Fiscal')
    concepto_id = columns.Integer('ID Concepto')
    tipo_impuesto = columns.Char('Tipo de Impuesto', size=50)
    base = columns.Float('Base')
    impuesto = columns.Char('Clave impuesto')
    tipo_factor = columns.Char('Tipo Factor')
    tasa_o_couta = columns.Float('Tasa o Cuota')
    importe = columns.Float('Importe')

