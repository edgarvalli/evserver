def run():
    from app import app
    from utils.tools import get_config

    config = get_config()
    app.config["app_config"] = config
    app.run(**config["app"])


if "__main__" == __name__:
    run()
