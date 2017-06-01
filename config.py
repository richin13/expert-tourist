import os


class BaseConfig:
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 12
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/dev.sqlite'.format(os.path.abspath(os.path.dirname(__file__)))


class TestConfig(DevConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''  # os.environ['PGSQL_URI']
