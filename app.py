import os
from flask import Flask
from importlib import import_module
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'p4ssw0rd')

jwt = JWTManager(app)

app.register_blueprint(import_module('controllers').api)