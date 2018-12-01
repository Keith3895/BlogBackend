import os



class BaseConfig(object):
    DEBUG = False
    TESTING = False
    MONGOALCHEMY_CONNECTION_STRING ='mongodb://localhost:27017/'
    MONGOALCHEMY_DATABASE = "pyTest"
    MONGODB_URL ='mongodb://localhost:27017/pyTest'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True




config = {
    "development": "blogREST.config.DevelopmentConfig",
    "testing": "blogREST.config.TestingConfig",
    "default": "blogREST.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    # app.config.from_pyfile('config.cfg', silent=True)