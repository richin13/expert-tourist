import os


class BaseConfig:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 12
    MONGODB_SETTINGS = {
        'db': '',
    }


class DevConfig(BaseConfig):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'dev-db',
    }


class TestConfig(BaseConfig):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'test-db',
    }


class ProductionConfig(BaseConfig):
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGODB_HOST_PROD', ''),
        'username': os.environ.get('MONGODB_USER_PROD', ''),
        'password': os.environ.get('MONGODB_PASSWORD_PROD', ''),
        'db': 'prod-db',
    }
