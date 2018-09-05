import os

from flask_jwt_extended import JWTManager

from app import create_app
from app.Models import API

# import configuration setting
config_name = os.getenv('APP_SETTINGS')

# inititlizre the app object
app = create_app(__name__, config_name)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')

# initialize JWT auth
jwt = JWTManager(app)

# initialize the api object
api = API(app, version='1.0', title='Fast-Food-Fast API',
          description="A food delivery service application API")
api.register_namespace()
app = api.app

if __name__ == '__main__':
    api.app.run()
