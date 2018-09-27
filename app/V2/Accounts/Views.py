from flask_jwt_extended import create_access_token
from flask_restplus import Resource, reqparse
from webargs.flaskparser import use_kwargs, use_args

from app.V1.Accounts.Models import UserSchema
from app.V2 import DB
from app.V2.Accounts.parsers import Parsers
from app.V2.decorators import *
from app.V2.Accounts.Models import User


@namespace.route('/register-user', endpoint="add-new-user")
class AddUser(Resource):
    """view for registering users"""

    @namespace.expect(Parsers().user)
    def post(self):
        """register new user to DB"""
        data = Parsers().user.parse_args()
        # validate input
        try:
            result = UserSchema().load(data)
        except ValidationError as error:
            DB.logger.error(str(error))
            return {'message': str(error)}, getattr(error, 'code', 401)

        # Add user to DB

        User().add_user(data)

        res = {
            "Message": "New user has been added",
            "details": result}
        return res


@namespace.route('/login-user', endpoint="authenticate-users")
class ValidateUser(Resource):
    """
    A class for validating user sesessions
    """

    @namespace.expect(Parsers().login)
    def post(self):
        """
        validate and return user session details
        :return: user, JWt token
        """
        data = Parsers().login.parse_args()
        # validate inputs
        try:
            UserSchema(only=('email', 'password')).load(data)
        except ValidationError as error:
            DB.logger.error(str(error))
            return {'message': str(error)}, getattr(error, 'code', 401)
        user = User().login_user(data['email'], data['password'])

        # assign tokens to user
        access_token = create_access_token(user)

        ret = dict(
            details=UserSchema().dump(user.user),
            access_token=access_token
        )

        return ret
