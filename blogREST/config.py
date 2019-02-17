import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    MONGOALCHEMY_CONNECTION_STRING ='mongodb://localhost:27017/'
    MONGOALCHEMY_DATABASE = "blog-api"
    MONGODB_URL ='mongodb://keimo:keimo123@ds141924.mlab.com:41924/blog-db'


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