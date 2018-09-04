import os

from app import create_app
from app.Models import API

# import configuration setting
config_name = os.getenv('APP_SETTINGS')

# inititlizre the app object
app = create_app(__name__, config_name)

# initialize the api object
api = API(app, version='1.0', title='Fast-Food-Fast API',
          description="A food delivery service application API")
api.register_namespace()
app = api.app

if __name__ == '__main__':
    api.app.run()
