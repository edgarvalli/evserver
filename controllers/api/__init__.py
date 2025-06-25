from utils.db import mysql
from flask import Blueprint,request

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
def api_index():
    return {
        'error': False,
        'message': 'API de EVAPP'
    }

@api.route('/<model>')
def api_search(model: str):
    return {
        'error': False,
        'data': mysql.search(model=model, **request.args)
    }