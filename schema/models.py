from lib.evschema import models, columns

class ModelsShema(models.Model):
    _name = 'models'
    _description = 'Table where store modules'

    name = columns.Char(label='Module', size=50, unique=True)
    description = columns.Char(label='Description')
    active = columns.Bool('Activo')

class ProfileModels(models.Model):

    _name = 'group_models'
    _description = 'Table with relationship between group and models'

    profile_id = columns.Integer('GroupID')
    model_id = columns.Integer('ModelID')
    perm_read = columns.Bool('Read')
    perm_write = columns.Bool('Write')
    perm_delete = columns.Bool('Delete')