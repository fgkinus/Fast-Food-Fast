from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restplus import Resource
from marshmallow import ValidationError

from app.V1.Accounts.Models import UserSchema
from app.V2 import DB
from app.V2.Accounts.parsers import Parsers
from app.V2.decorators import *
from app.V2.Accounts.Models import User


@namespace.route('/signup', endpoint="add-new-user")
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


@namespace.route('/register-admin', endpoint="add-new-admin")
class AddAdmin(Resource):
    """view for registering new admins"""

    @admin_required
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

        User().add_admin(data)

        res = {
            "Message": "New user has been added",
            "details": result}
        return res


@namespace.route('/login', endpoint="authenticate-users")
class ValidateUser(Resource):
    """
    A class for validating user sessions
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


@namespace.route('/profile', endpoint='User profile')
class UserProfile(Resource):
    """User profile related actions"""

    @jwt_required
    def get(self):
        """
        Get and return the details of the currently logged in user
        :return: user
        """
        user = get_jwt_identity()
        user_details = User().get_user_by_username(user)
        ret = dict(
            user_details=UserSchema().dump(user_details)
        )
        return ret

    @jwt_required
    @namespace.expect(Parsers().user)
    def put(self):
        """
        Edit a currently logged in user's details
        :return:
        """
        user = get_jwt_identity()
        user_details = User().get_user_by_username(user)

        data = Parsers().user.parse_args()
        modified = User().edit_user(user_details, data)
        ret = dict(
            details=UserSchema().dump(modified)
        )
        return ret
