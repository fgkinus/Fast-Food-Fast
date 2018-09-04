from flask_restplus import Api


class API:
    """Initialize the app object and the associated API"""
    app = None
    api = None

    def __init__(self, app, **kwargs):
        """Initialize the object"""
        self.app = app
        self.__create_api(**kwargs)

    def __create_api(self, **kwargs):
        """initialize an instance of the flask rest plus API"""
        self.api = Api(self.app)
        self.set_attr(**kwargs)

    def set_attr(self, **kwargs):
        # dynamicaly set class attributes
        if kwargs:
            for key, value in kwargs.items():
                try:
                    setattr(self.api, key, value)
                except:
                    self.app.logger.info("attribute could not be set")

    def register_namespace(self, name_space, path):
        """recognise url endpoints"""
        self.api.add_namespace(name_space, path=path)
