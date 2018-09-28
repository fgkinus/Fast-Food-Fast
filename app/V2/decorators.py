# Create a function that will be called whenever create_access_token
from functools import wraps

import marshmallow
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restplus import Namespace
from jwt import ExpiredSignature, InvalidSignatureError

from app import jwt
from app.Exceptions import AlreadyExists

namespace = Namespace('Auth', description='user accounts authentication and registration')


# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what custom claims
# should be added to the access token.
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'admin': user.get_admin_status()}


# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what the identity
# of the access token should be.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.user['username']


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['admin'] is False:
            return {'msg': "Admin Users only!!!"}, 401
        else:
            return fn(*args, **kwargs)

    return wrapper


# error handlers
@namespace.errorhandler(NoAuthorizationError)
def handle_no_auth_exception(error):
    """Handle ethe jwt required exception when none s provided"""
    return {'message': 'No authentication token provided'}, 401


@namespace.errorhandler(ExpiredSignature)
def handle_expired_token(error):
    return {'message': 'authentication token provided is expired'}, 401


@namespace.errorhandler(InvalidSignatureError)
def handle_expired_token(error):
    return {'message': 'authentication token provided is invalid'}, 401


@namespace.errorhandler(LookupError)
def handle_expired_look_up_error(error):
    """To allow for a custom message, status 200 is used instead of 204"""
    return {'message': 'The item you are looking for was not found'}, 200


@namespace.errorhandler(AlreadyExists)
def handle_already_exists_exception(error):
    """Handle handle the already exists error"""
    return {'message': error.message}, getattr(error, 'code', 500)


@namespace.errorhandler(marshmallow.exceptions.ValidationError)
def handle_validation_exception(error):
    """Handle handle the already exists error"""
    return {"error message"}, 500  # {'message': error.message}, getattr(error, 'code', 500)


@namespace.errorhandler
def default_error_handler(error):
    """Default error handler"""
    return {'message': str(error)}, getattr(error, 'code', 500)
