from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_restplus import Resource, reqparse, Namespace, inputs

# define a namespace for authentication and registration of users
from app.Accounts import Models
from .decorators import *


# register new user
@namespace.route('/register-user', endpoint="add-new-user")
class UserRegistration(Resource):
    # request parser
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('username', help='This field cannot be blank', required=True)
    request_parser.add_argument('first_name', help='This field cannot be blank', required=True)
    request_parser.add_argument('second_name', help='This field cannot be blank', required=True)
    request_parser.add_argument('email', help='This field cannot be blank', required=True,
                                type=inputs.email(check=True))
    request_parser.add_argument('password', help='This field cannot be blank', required=True)
    request_parser.add_argument('surname', help='This field cannot be blank', required=True)

    # model attributes
    username = None
    first_name = None
    second_name = None
    email = None
    password = None
    surname = None

    @namespace.expect(request_parser)
    def post(self):
        """add new admin user"""
        # initialise the request parser
        self.add_req_parsers()
        data = self.request_parser.parse_args()  # parse user input
        self.fetch_user_details(data=data)
        # create admin object
        user = Models.User().add_user(self.username, self.first_name, self.second_name, self.surname, self.password,
                                      self.email)

        return {
            'id': user.ID,
            'new-user': data
        }

    def add_req_parsers(self):
        self.request_parser.add_argument('username', help='This field cannot be blank', required=True)
        self.request_parser.add_argument('first_name', help='This field cannot be blank', required=True)
        self.request_parser.add_argument('second_name', help='This field cannot be blank', required=True)
        self.request_parser.add_argument('email', help='This field cannot be blank', required=True,
                                         type=inputs.email(check=True))
        self.request_parser.add_argument('password', help='This field cannot be blank', required=True)
        self.request_parser.add_argument('surname', help='This field cannot be blank', required=True)

    def fetch_user_details(self, data):
        """get parsed user details"""
        self.username = data['username']
        self.first_name = data['first_name']
        self.second_name = data['second_name']
        self.email = data['email']
        self.password = data['password']
        self.surname = data['surname']


# register new admin
@namespace.route('/register-admin', endpoint="add-new-admin")
class AdminRegistration(UserRegistration):
    """admin registration viewset"""
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('username', help='This field cannot be blank', required=True)
    request_parser.add_argument('first_name', help='This field cannot be blank', required=True)
    request_parser.add_argument('second_name', help='This field cannot be blank', required=True)
    request_parser.add_argument('email', help='This field cannot be blank', required=True,
                                type=inputs.email(check=True))
    request_parser.add_argument('password', help='This field cannot be blank', required=True)
    request_parser.add_argument('surname', help='This field cannot be blank', required=True)

    # request_parser = reqparse.RequestParser()
    @namespace.expect(request_parser)
    # @admin_required
    def post(self):
        """add new admin user"""
        # initialise the request parser
        self.add_req_parsers()
        data = self.request_parser.parse_args()  # parse user input
        self.fetch_user_details(data=data)
        # create admin object
        admin = Models.Admin().add_user(self.username, self.first_name, self.second_name, self.surname, self.password,
                                        self.email)

        return {
            'id': admin.ID,
            'new-user': data
        }


# login new user or admin
@namespace.route('/login', endpoint="Login")
class LoginUsers(Resource):
    """A view to authenticate all users"""
    email = None
    password = None
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('email', help='This field cannot be blank', required=True,
                                type=inputs.email(check=True))
    request_parser.add_argument('password', help='This field cannot be blank', required=True)

    def add_req_parsers(self):
        self.request_parser.add_argument('email', help='This field cannot be blank', required=True)
        self.request_parser.add_argument('password', help='This field cannot be blank', required=True)

    def fetch_user_details(self, data):
        """get parsed user details"""
        self.email = data['email']
        self.password = data['password']

    @namespace.expect(request_parser)
    def post(self):
        """add new admin user"""
        # initialise the request parser
        self.add_req_parsers()
        data = self.request_parser.parse_args()  # parse user input
        self.fetch_user_details(data=data)

        user = Models.Admin().add_user(username='testadmin', firstname='firstname', surname='sir', secondname='second',
                                       password='pass',
                                       email='testadmin@test.com')
        # search users
        user = Models.User().get_user(email=self.email, password=self.password)
        admin = Models.Admin().get_user(email=self.email, password=self.password)

        # alert if user is not found
        if user is False and admin is False:
            return {
                       'message': "wrong user or password"
                   }, 401
        else:
            # if user is a normal user authenticate
            if user is not False:
                access_token = create_access_token(identity=user)
                ret = {'access_token': access_token, 'details': dict(
                    username=user.username,
                    email=user.email
                )}
                return jsonify(ret)

            elif admin is not False:
                access_token = create_access_token(identity=admin)
                ret = {'access_token': access_token, 'details': dict(
                    username=admin.username,
                    email=admin.email
                )}
                return jsonify(ret)

            else:
                return jsonify(mes="None")
