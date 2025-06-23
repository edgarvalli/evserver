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
            from utils.dbtool import createdb

            createdb(config)
            return _mysql_connector.connect(**config)

        raise e
    except KeyError as e:
        raise e


def insert_all_paths():

    sql = get_mysql_connection()
    sql.autocommit = True
    cursor = sql.cursor(dictionary=True)
    query = "SELECT COUNT(id) total FROM endpoints"
    cursor.execute(query)

    t: dict = cursor.fetchone()
    path_ids = []

    if t.get("total", 0) == 0:
        query = "SELECT id FROM roles WHERE name='master'"
        cursor.execute(query)
        role: dict = cursor.fetchone()
        role = role.get("id", 0)

        query = "INSERT IGNORE INTO endpoints (path,public) VALUES (%s,0)"

        for url in current_app.url_map.iter_rules():
            print(url)
            cursor.execute(query, (url.rule,))
            path_ids.append((role, cursor.lastrowid))

    cursor.close()
    sql.close()
