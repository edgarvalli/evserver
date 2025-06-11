from lib.evschema import DBConfig

class dbtool:

    @staticmethod
    def dbconfig() -> DBConfig:
        from pathlib import Path

        cwd = Path(__file__).parent.parent
        config_filename = cwd.joinpath("config.json")

        with open(config_filename, "r", encoding="utf-8") as f:
            import json

            config = json.loads(f.read())
            config: dict = config["dbconfig"]

        dbconfig = DBConfig()
        dbconfig.dbhost = config.get("host", "localhost")
        dbconfig.dbuser = config.get("user", "root")
        dbconfig.dbpass = config.get("password", "p4ssw0rd")
        dbconfig.dbport = config.get("port", 3306)
        dbconfig.dbname = config.get("database", "mysql")

        return dbconfig

    @staticmethod
    def createdb():
        from lib.evschema import EVSchema
        import importlib, inspect
        from pathlib import Path

        dbconfig = dbtool.dbconfig()
        evschema = EVSchema(dbconfig.dbname, dbconfig)
        cwd = Path(__file__).parent.parent

        if evschema.database_exists():
            return print(f"La base de datos [{evschema.dbname}] ya existe!!!!")

        print("Iniciando creacion de base de datos " + evschema.dbname)
        evschema.import_models_from_path(cwd.joinpath('schema'))
        if evschema.createdb():
            evschema.inflate_from_csv(cwd.joinpath('data'))
            print(f"{evschema.dbname} ha sido creada")
