import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent settings file"""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_URL')
    BUNDLE_ERRORS = True
    RESTPLUS_VALIDATE = True
    SWAGGER_UI_JSONEDITOR = True
    SWAGGER_UI_DOC_EXPANSION = 'list'
    CORS_HEADERS = 'Content-Type'

    # JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = False


class TestingConfig(Config):
    """Configurations for Testing"""

    TESTING = True
    DATABASE_URL = os.getenv('TESTING_DB_URL')
    JWT_REFRESH_TOKEN_EXPIRES = False


class StagingConfig(Config):
    """Configurations for staging"""

    DEBUG = True
    DEVELOPMENT = True


class ProductionConfig(Config):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False


APP_CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
