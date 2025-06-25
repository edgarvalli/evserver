from lib.evschema import Model, columns

class RegimenFiscal(Model):
    _name = 'regimenes_fiscales'

    codigo = columns.Char('Codigo', size=10)
    descripcion = columns.Char('Nombre Regimen', size=200)
    tipo = columns.Char('Tipo', size=300)
    tipo_codigo = columns.Integer('TipoID')

class MetodoPago(Model):
    _name = "metodo_pago"

    codigo = columns.Char('Metodo de Pago Codigo', size=10)
    descripcion = columns.Char('Metodo de Pago', size=100)