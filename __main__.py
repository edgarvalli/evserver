import os
from app import app


def main():

    config_filename = "config.json"
    if not os.path.exists(config_filename):
        raise ValueError(
            """
            Debe de crear el archivo config.json con la siguiente configuracion:

            {
                "host": "0.0.0.0",
                "port": 5000,
                "debug": true,
                "dbconfig": {
                    "host": "localhost",
                    "user": "root",
                    "password": "",
                    "database": "evdb"
                }
            }
        """
        )

    config: dict = {}

    with open(config_filename, "r", encoding="utf-8") as f:
        import json
        from utils import dbtool
        
        config = json.loads(f.read())
        app.config["app_config"] = config
    

        dbtool.createdb()
    
        app.run(
            host=config['host'],
            port=config['port'],
            debug=config['debug']
        )


if __name__ == "__main__":
    main()
