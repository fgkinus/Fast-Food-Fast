from flask_jwt_extended import JWTManager
from flask_restplus import Api, abort

from app.Exceptions import AttributeNotFound


class API:
    """Initialize the app object and the associated API"""
    app = None
    api = None
    jwt = None

    def __init__(self, app, jwt, **kwargs):
        """Initialize the object"""
        self.app = app
        self.jwt = jwt
        self.__create_api(**kwargs)
        jwt = self.__init_jwt()

    def __create_api(self, **kwargs):
        """initialize an instance of the flask rest plus API"""
        self.api = Api(self.app)
        self.set_attr(**kwargs)

    def set_attr(self, **kwargs):
        # dynamically set class attributes
        if kwargs:
            for key, value in kwargs.items():
                if not hasattr(self.api, key):
                    self.app.logger.info("attribute could not be set")
                    raise AttributeNotFound("attribute %s not defined", key)
                else:
                    try:
                        setattr(self.api, key, value)
                    except AttributeError:
                        self.app.logger.info("attribute could not be set")
                        abort(500, "Could not set the attribute {0}".format(key))

    def register_namespace(self, namespace, path):
        """recognise url endpoints"""
        self.api.add_namespace(namespace, path)
        return self.api

    def __init_jwt(self):
        self.jwt.init_app(self.app)
        return self.jwt


class URLS:
    """a class for handling url routing"""

    def __init__(self, api, urls):
        # initialize the class
        self.api = api
        self.urls = urls
        self.__register()

    def __register(self):
        # Iteratively register urls
        for url in self.urls.items():
            self.api.register_namespace(namespace=url[0], path=url[1])

    def get_api(self):
        """return the api object"""
        return self.api
