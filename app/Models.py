from flask import Flask
from flask_restplus import Api

from config import APP_CONFIG, basedir


class App:
    """Initialize the app object and the associated API"""
    app = None
    api = None

    def __init__(self, name, config_name='development'):
        """Initialize the object"""
        self.app = self.__create_app(name, config_name)
        self.__create_api()

    @staticmethod
    def __create_app(name, config_name):
        """create an instance of the flask app object"""
        app = Flask(name)
        app.config.from_object(APP_CONFIG[config_name])
        app.config.from_pyfile(basedir, 'config.py')
        return app

    def __create_api(self):
        """initialize an instance of the flask rest plus API"""
        self.api = Api(self.app, version='1.0',
                       title='API')

    def register_namespace(self, name_space, path):
        """recognise url endpoints"""
        self.api.add_namespace(name_space, path=path)
