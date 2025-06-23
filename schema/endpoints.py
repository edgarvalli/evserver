from lib.evschema import models, columns

class Endpoints(models.Model):
    _name = 'endpoints'
    _description = 'Table where store all endpoint from flask'

    path = columns.Char('Url Path', size=300, unique=True, index=True)
    description = columns.Char('Url Path Description', size=200)
    public = columns.Bool('Is Public', default=0)
    active = columns.Bool('Is Active', default=1)

class EnpointRoles(models.Model):
    _name = 'endpoint_roles'
    _description = 'Table where store relationship between roles and endpoints'

    role_id = columns.Integer('Role ID')
    endpoint_id = columns.Integer('Endpoint ID')