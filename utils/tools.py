from pathlib import Path
import mysql.connector as _mysql_connector
from flask import current_app


def get_root_path() -> Path:
    if current_app:
        return current_app.root_path
    else:
        path = Path(__file__).parent.parent
        return path


def get_config(config_file: str = "app.conf") -> dict:
    if current_app:
        return current_app.config["app_config"]
    else:
        from configparser import ConfigParser

        parser = ConfigParser()
        parser.read(str(get_root_path().joinpath(config_file)))
        config = {}
        for section in parser.sections():
            config[section] = {}
            for key, value in parser[section].items():
                config[section][key] = value

        debug = config["app"]["debug"]
        debug = True if int(debug) == 1 else False
        config["app"]["debug"] = debug

        return config


def get_mysql_connection() -> _mysql_connector.MySQLConnection:

    config = get_config()
    config = config["mysql"]

    try:
        return _mysql_connector.connect(**config)

    except _mysql_connector.errors.ProgrammingError as e:
        if e.errno == 1049:
            dbname = config["database"]
            del config["database"]
            cxn = _mysql_connector.connect(**config)
            cursor = cxn.cursor()
            cursor.execute("CREATE DATABASE " + dbname)
            cxn.commit()
            cursor.close()
            cxn.database = dbname
            return cxn

        raise e
    except:
        raise "Ocurrio un error desconocido en mysql"
