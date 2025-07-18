from utils.db import mysql
from flask import Blueprint,request
from importlib import import_module

api = Blueprint('api', __name__, url_prefix='/api')

api.register_blueprint(import_module('controllers.api.clients').client_router)
api.register_blueprint(import_module('controllers.api.documentos').doc_router)

@api.route('/')
def api_index():
    return {
        'error': False,
        'message': 'API de EVAPP'
    }

@api.route('/<model>')
def api_search(model: str):

    response = mysql.search(model=model, **request.args)

    return {
        'error': False,
        'data': response.get('result'),
        'total_rows': response.get('total_rows',0)
    }

@api.route('/<model>/save', methods=['POST'])
def api_save(model: str):

    if "application/json" in request.headers['Content-Type']:
        data = request.json
        files = None

    else:
        data = request.form
        files = request.files
    
    print(data, files)

    return {
        'error': True,
        'message': 'In DEV'
    }