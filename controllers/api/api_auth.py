from flask import Blueprint

api_auth = Blueprint('api_login', __name__, url_prefix='/auth')

@api_auth.route('/sing')
def api_sign():
    return 'Work'