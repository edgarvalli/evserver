from flask import Blueprint, send_file

app_router = Blueprint('app_router', __name__, url_prefix='/app')

@app_router.route('/<path:subpath>')
def app_index(subpath: str):
    return send_file('fronted/dist/index.html')

@app_router.route('/assets/<filename>')
def app_assets(filename: str):
    return send_file('fronted/dist/assets/' + filename)