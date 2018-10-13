import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

from instance.config import APP_CONFIG, basedir

jwt = JWTManager()


def create_app(name, config_name):
    """create an instance of the flask APP object"""
    app = Flask(name,
                template_folder='UI/templates',
                static_folder='UI/static'
                )
    CORS(app=app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile(os.path.join(basedir, 'config.py'))
    return app
