from flask import Blueprint,current_app
from lib.mysqlsdk import MySQL

api_common = Blueprint('api_common', __name__)

@api_common.route('/<dbname>/<model>/')
def api_common_index(dbname: str = None, model: str = None):
    
    if model is None:
        return {
            'error': True,
            'message': 'Debe definir un modelo.'
        }
    
    
    dbconfig = current_app.config['app_config']['dbconfig']
    print(dbconfig)
    if dbname is None:
        dbname = dbconfig['database']
    
    query = f"SELECT * FROM {dbname}.{model}"
    
    
    _mysql = MySQL(**dbconfig)
        
    return _mysql.fetchall(model).__dict__