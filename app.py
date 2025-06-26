from flask import Flask, render_template
from importlib import import_module
import os

app = Flask(__name__)

app.secret_key = os.environ.get('APP_SECRET_KEY', 'p4ssw0rd')
app.config['UPLOAD_FOLDER'] = os.environ.get('APP_UPLOAD_FOLDER','filestore')

app.register_blueprint(import_module('controllers.api').api)
app.register_blueprint(import_module('controllers.app').app_router)

@app.route('/')
def index():
    from utils.tools import get_mysql_connection

    cxn = get_mysql_connection()
    
    cxn.close()
    return render_template('index.html')