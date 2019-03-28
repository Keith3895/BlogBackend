import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    MONGODB_URL = os.getenv('mongourl')
    MONGO_URI = os.getenv('mongourl')


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    secret_key = os.getenv('secret_key')
    client_id= os.getenv('client_id')
    client_secret= os.getenv('client_secret')


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    secret_key = os.getenv('secret_key')



config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    # return config
    # app.config.from_pyfile('config.cfg', silent=True)