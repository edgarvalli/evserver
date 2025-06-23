def run():
    from app import app
    from utils.tools import get_config, insert_all_paths

    config = get_config()
    app.config["app_config"] = config

    with app.app_context():
        insert_all_paths()

    app.run(**config["app"])


if "__main__" == __name__:
    run()
