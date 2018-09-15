from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restplus import Namespace
from jwt import ExpiredSignature

from app.Exceptions import AlreadyExists


class ExceptionHandler:
    """
    A class to contain all exception handlers for the api
    """
    namespace = Namespace('default')  # initialise the default name space

    def __init__(self, namespace):
        """
        the class initializer
        """
        if isinstance(namespace, Namespace):
            self.namespace = namespace

    @staticmethod
    @namespace.errorhandler(ExpiredSignature)
    def handle_expired_token(error):
        return {'message': 'authentication token provided is expired'}, 401

    @staticmethod
    @namespace.errorhandler(NoAuthorizationError)
    def handle_no_auth_exception(error):
        """Handle ethe jwt required exception when none s provided"""
        return {'message': 'No authentication token provided'}, 401

    @staticmethod
    @namespace.errorhandler(AlreadyExists)
    def handle_already_exists_exception(error):
        """Handle handle the already exists error"""
        return {'message': error.message}, getattr(error, 'code', 500)
