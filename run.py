import os

import coloredlogs

from app import create_app, jwt
from app.Models import API, URLS
from app.urls import urls_v2


# configure logging globally
coloredlogs.install()

# import configuration setting
config_name = os.getenv('APP_SETTINGS')

# initialize the app object
app = create_app(__name__, config_name)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')

# initialize the api object
api = API(app, jwt, version='2.0', title='Fast-Food-Fast API',
          description="A food delivery service application API")

# register urls_v1
api = URLS(api, urls_v2).get_api()

app = api.app


if __name__ == '__main__':
    app.run()
