import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent settings file"""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    TESTING = False
    DATABASE_URL = os.getenv('DB_URL')


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


