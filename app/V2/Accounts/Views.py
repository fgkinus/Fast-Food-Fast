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
        return result
