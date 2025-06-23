from lib.evschema import models, columns

class Menus(models.Model):

    _name = 'menus'
    _description = 'Menu Table'

    menu_key = columns.Char(label='Menu Key', size=100, unique=True, index=True)
    name = columns.Char(label='Menu Name', size=200)
    path = columns.Char(label='Path', size=200)
    icon = columns.Char(label='Icon', size=50)
    description = columns.Char(label='Description', size=200)
    parent_id = columns.Integer(label='ParentID')
    parent_key = columns.Char(label='ParentKEY', size=100, index=True)
    sequence = columns.Integer(label='Sequence')
    active = columns.Bool('Activo')

class MenuRoles(models.Model):

    _name = 'menu_roles'
    _description = 'Table with relationship between Menu and Roles'

    menu_id = columns.Integer(label='MenuID')
    role_id = columns.Integer(label='GroupID')