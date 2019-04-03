import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


class BaseConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.getenv('secret_key')
    MONGODB_URL = os.getenv('mongourl')
    MONGO_URI = os.getenv('mongourl')

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SECRET_KEY = os.getenv('secret_key_test')


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
    "production": DevelopmentConfig
}


def configure_app(app):
    config_name = os.getenv('Flask_Env', 'default')
    app.config.from_object(config[config_name])
    # return config
    # app.config.from_pyfile('config.cfg', silent=True)
