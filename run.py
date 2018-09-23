import os
import subprocess

import coloredlogs

from app import create_app, jwt
from app.Models import API, URLS
from app.urls import urls
from app.V2 import DB  # this import initialises the DB connection

# configure logging globally
coloredlogs.install()

# import configuration setting
config_name = os.getenv('APP_SETTINGS')

# initialize the app object
app = create_app(__name__, config_name)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')

# initialize the api object
api = API(app, jwt, version='1.0', title='Fast-Food-Fast API',
          description="A food delivery service application API")

# register urls
api = URLS(api, urls).get_api()

app = api.app

if __name__ == '__main__':
    api.app.run()
