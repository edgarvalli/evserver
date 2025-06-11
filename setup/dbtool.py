from tool import set_project_path
cwd = set_project_path()

from lib.evschema import EVSchema, DBConfig, Database

class dbtool:

    @staticmethod
    def dbconfig() -> DBConfig:
        config_filename = cwd.joinpath("config.json")

        with open(config_filename, 'r', encoding='utf-8') as f:
            import json
            config = json.loads(f.read())
            config:dict = config['dbconfig']

        dbconfig = DBConfig()
        dbconfig.dbhost = config.get('host','localhost')
        dbconfig.dbuser = config.get('user','root')
        dbconfig.dbpass = config.get('password','p4ssw0rd')
        dbconfig.dbport = config.get('port',3306)
        dbconfig.dbname = config.get('database', 'mysql')

        return dbconfig

    @staticmethod
    def rebuild():

        dbconfig = dbtool.dbconfig()

        print("Limpiando base de datos")
        db = Database(dbconfig)
        db.query("DROP DATABASE " + dbconfig.dbname)
        evschema = EVSchema(dbconfig.dbname, dbconfig)

        print("Iniciando creacion de base de datos " + evschema.dbname)
        evschema.import_models_from_path(cwd.joinpath('schema'))
        if evschema.createdb():
            evschema.inflate_from_csv(cwd.joinpath('data'))
            print(f"{evschema.dbname} ha sido creada")