from utils.db import mysql, _mysql_errors
from flask import Blueprint, request, jsonify

# from utils.tools import get_root_path
clients_route = Blueprint("clients_route", __name__, url_prefix="/clients")


@clients_route.errorhandler(ValueError)
def handle_value_error(e: ValueError):
    return jsonify({"error": True, "message": e.args[0], "status_code": 400})


@clients_route.route("/")
def clients_search():
    print(clients_route.root_path)
    query = "SELECT c.id,c.name,c.email,c.rfc, a.address,a.zip_code " \
    "FROM clients AS c, address AS a " \
    "WHERE a.rel_id = c.id AND a.rel_model = 'clients'"

    query = """
        SELECT c.id,c.name,c.email,c.rfc, a.address,a.zip_code,
        rf.descripcion regimen_fiscal, rf.codigo regimen_fiscal_codigo,
        mp.descripcion metodo_pago, mp.codigo metodo_pago_codigo
        FROM clients AS c, address AS a, regimenes_fiscales AS rf, metodo_pago AS mp
        WHERE a.rel_id = c.id AND a.rel_model = 'clients'
        AND c.regimen_fiscal_id = rf.id AND mp.id = c.metodo_pago_id
    """

    try:

        data = mysql.fetchall(query)
        return {"error": False, "data": data}
    except _mysql_errors.ProgrammingError as e:
        raise ValueError(f"Mysql Error[{e.errno}]: {e.msg}")


@clients_route.route("/save", methods=["POST"])
def clients_route_save():
    data = {}
    files = request.files

    # Se limpia todos los valores de la dirección
    address = {"rel_id": 0, "rel_model": "clients"}

    for key, val in request.form.items():
        if key.startswith("a_"):
            _key = key.replace("a_", "")
            address[_key] = val
        else:
            data[key] = val
    try:
        result = mysql.save("clients", **data)
        id = result.get("lastrowid", None)

        if id is not None:
            address["rel_id"] = id
            mysql.save("address", **address)
            for file in files:
                file = files[file]
                filename = file.filename
                file.save(filename)

        return {"error": False, "message": ""}
    except _mysql_errors.ProgrammingError as e:
        print(e)
        raise ValueError(f"Mysql Error[{e.errno}]: {e.msg}")
    except ValueError:
        raise ValueError("Ocurrio un error")
