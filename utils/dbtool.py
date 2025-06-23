def createdb(config: dict):
    from lib.evschema import EVSchema, DBConfig
    from pathlib import Path
    
    # dbname = config.get('database',None)
    # if dbname is None:
    #     raise 'Debe de definir un nombre de base de datos.'
    
    # del config['database']

    config = DBConfig(**config)
    evschema = EVSchema(config)
    # evschema.dbname = dbname
    cwd = Path(__file__).parent.parent

    if evschema.database_exists():
        return print(f"La base de datos [{evschema.dbname}] ya existe!!!!")

    print("Iniciando creacion de base de datos " + evschema.dbname)
    evschema.import_models_from_path(cwd.joinpath("schema"))
    if evschema.createdb():
        evschema.inflate_from_csv(cwd.joinpath("data"))
        print(f"{evschema.dbname} ha sido creada")
