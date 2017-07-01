import os
import datetime


class BaseConfig:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 12
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_HEADER_TYPE = ''
    MONGODB_SETTINGS = {
        'db': '',
    }


class DevConfig(BaseConfig):
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
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
        'host': os.environ.get('MONGODB_URI', ''),
    }
