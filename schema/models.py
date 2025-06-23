from lib.evschema import models, columns

class ModelsShema(models.Model):
    _name = 'models'
    _description = 'Table where store modules'

    name = columns.Char(label='Module', size=50, unique=True)
    description = columns.Char(label='Description')
    active = columns.Bool('Activo')

class ModelRoles(models.Model):

    _name = 'model_roles'
    _description = 'Table with relationship between roles and models'

    role_id = columns.Integer('GroupID')
    model_id = columns.Integer('ModelID')
    perm_read = columns.Bool('Read')
    perm_write = columns.Bool('Write')
    perm_delete = columns.Bool('Delete')