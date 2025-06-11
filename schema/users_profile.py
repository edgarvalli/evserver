from lib.evschema import models, columns

class Users(models.Model):
    _name = 'users'
    _description = 'Users Table'

    username = columns.Char(label='Username', size=50, unique=True)
    email = columns.Char(label='Email', size=100, unique=True)
    password_hash = columns.Char(label='PasswordHashed', size=200)
    displayname = columns.Char(label='DisplayName', size=300)
    active = columns.Bool('Activo')

class Profiles(models.Model):
    _name = 'profiles'
    _description = 'Profiles Table'

    name = columns.Char(label='Group Name', size=100)
    description = columns.Char(label='Group Description', size=100)
    active = columns.Bool('Activo')

class UserGroups(models.Model):

    _name = 'user_groups'
    _description = 'Table with relationship with user and groups'

    user_id = columns.Integer('ModelID')
    profile_id = columns.Integer('GroupID')
    perm_read = columns.Bool('Read')
    perm_write = columns.Bool('Write')
    perm_delete = columns.Bool('Delete')