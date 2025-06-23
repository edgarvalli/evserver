from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    from utils.tools import get_mysql_connection

    cxn = get_mysql_connection()
    
    cxn.close()
    return render_template('index.html')