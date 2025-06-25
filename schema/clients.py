from lib.evschema import Model, columns


class Clients(Model):
    _name = "clients"
    _description = "Clients Module"

    name = columns.Char("Nombre del Cliente", size=200)
    email = columns.Char("Correo", size=100)
    rfc = columns.Char("Rfc", size=18, unique=True)
    razon_social = columns.Char("Razon Social", size=200)
    uso_cfdi = columns.Integer("ID Uso de CFDI")
    metodo_pago_id = columns.Integer("ID Metodo Pago")
    regimen_fiscal_id = columns.Integer("ID Regimen Fiscal")


class Address(Model):
    _name = "address"

    rel_id = columns.Integer("ID Objeto", index=True)
    rel_model = columns.Char("Tabla Relación", index=True)
    address = columns.Char("Dirección", size=200)
    zip_code = columns.Char("Codigo Postal")
    city = columns.Char("Ciudad")
    state = columns.Char("Estado")
    country = columns.Char("Pais")
