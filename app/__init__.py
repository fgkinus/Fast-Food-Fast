import os

from flask import Flask
from flask_jwt_extended import JWTManager

from config import APP_CONFIG, basedir

jwt = JWTManager()


def create_app(name, config_name):
    """create an instance of the flask app object"""
    app = Flask(name)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile(os.path.join(basedir, 'config.py'))
    return app
