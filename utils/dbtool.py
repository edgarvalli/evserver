from lib.evschema import EVSchema, DBConfig
from utils.tools import get_mysql_connection, get_config, get_root_path

def createdb(config: dict):

    config = DBConfig(**config)
    evschema = EVSchema(config)

    cwd = get_root_path()

    if evschema.database_exists():
        return print(f"La base de datos [{evschema.dbname}] ya existe!!!!")

    print("Iniciando creacion de base de datos " + evschema.dbname)
    evschema.import_models_from_path(cwd.joinpath("schema"))
    if evschema.createdb():
        evschema.inflate_from_csv(cwd.joinpath("data"))
        print(f"{evschema.dbname} ha sido creada")

def rebuild():

    config:dict = get_config()['mysql']
    dbname = config.get('database', None)
    cwd = get_root_path()

    if dbname is None:
        raise ValueError('No esta la base de datos definida.')

    print("Limpiando base de datos")
    try:
        sql = get_mysql_connection()
        cursor = sql.cursor()
        cursor.execute(f"DROP DATABASE {dbname}")
        dbconfig = DBConfig(**config)
        evschema = EVSchema(dbconfig)

        print("Iniciando creacion de base de datos " + evschema.dbname)
        evschema.import_models_from_path(cwd.joinpath("schema"))
        if evschema.createdb():
            evschema.inflate_from_csv(cwd.joinpath("data"))
            print(f"{evschema.dbname} ha sido creada")
            dbconfig.database = evschema.dbname
            create_relationship_roles(dbconfig)
        
        cursor.close()

    except KeyError as e:
        raise ValueError(e)

def create_relationship_roles(config: DBConfig = None):
    if config is None:
        raise ValueError('Debe definir los parametros de configuracion.')

    dbname = config.database

    try:
        sql = get_mysql_connection()
        cursor = sql.cursor()

        sql.autocommit = True


        query = f"SELECT id FROM {dbname}.roles WHERE name='master'"
        cursor.execute(query)

        role = cursor.fetchone()
        role = role[0]

        users_admin = ["admin"]

        for useradmin in users_admin:
            query = f"SELECT id FROM {dbname}.users WHERE username='{useradmin}'"
            cursor.execute(query)

            user = cursor.fetchone()

            if user is not None:
                query = f"INSERT INTO {dbname}.user_roles (user_id, role_id, perm_write, perm_read,perm_delete) VALUES (%s,%s,1,1,1)"
                cursor.execute(query, (user[0],role))

        query = f"SELECT id FROM {dbname}.menus"
        cursor.execute(query)

        menu_ids = [(role, item[0]) for item in cursor]

        query = f"INSERT INTO {dbname}.menu_roles (role_id, menu_id) VALUES (%s,%s)"
        cursor.executemany(query, menu_ids)

        cursor.close()
        sql.close()
    except KeyError as e:
        raise ValueError(e)