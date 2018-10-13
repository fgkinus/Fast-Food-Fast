"""The application's entry point"""

import os

import coloredlogs
from flask import render_template

from app import create_app, jwt
from app.Models import API, URLS
from app.urls import urls_v2

# configure logging globally
coloredlogs.install()

# import configuration setting
CONFIG_NAME = os.getenv('APP_SETTINGS')

# initialize the APP object
APP = create_app(__name__, CONFIG_NAME)
APP.config['JWT_SECRET_KEY'] = os.getenv('SECRET')


@APP.route('/<page_name>')
def render_static(page_name):
    try:
        return render_template('{0}'.format(page_name))
    except:
        return render_template('error404.html')


# initialize the API object
API = API(APP, jwt, version='2.0', title='Fast-Food-Fast API',
          description="A food delivery service application API")

# register urls_v1
API = URLS(API, urls_v2).get_api()

APP = API.app

if __name__ == '__main__':
    APP.run()
