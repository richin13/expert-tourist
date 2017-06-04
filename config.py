import os


class BaseConfig:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 12
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/dev.sqlite'.format(BaseConfig.BASEDIR)


class TestConfig(DevConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/test.sqlite'.format(BaseConfig.BASEDIR)


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''  # os.environ['PGSQL_URI']
