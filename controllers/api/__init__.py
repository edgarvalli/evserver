from flask import Blueprint
from importlib import import_module
from flask_jwt_extended import create_access_token


def make_import_path(module: str):
    return "controllers.api." + module


api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(import_module(make_import_path("api_auth")).api_auth)
api.register_blueprint(import_module(make_import_path("api_common")).api_common)



@api.route("/")
def api_index():
    token = create_access_token(identity="admin")
    return {"error": False, "message": "EVAPP API WORKS!!!", "token": token}
