from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_restplus import Resource, reqparse, Namespace

# define a namespace for authentication and registration of users
from app.Accounts import Models

# Create a function that will be called whenever create_access_token
from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

from run import jwt


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
    return user.username


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['admin'] is False:
            return jsonify(msg="Admin Users only!!!"), 401
        else:
            return fn(*args, **kwargs)

    return wrapper


# api name space
namespace = Namespace('Auth', description='user accounts authentication and registration')


# register new user
@namespace.route('/register-user', endpoint="add-new-user")
class UserRegistration(Resource):
    request_parser = reqparse.RequestParser()
    username = None
    first_name = None
    second_name = None
    email = None
    password = None
    surname = None

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
        self.request_parser.add_argument('email', help='This field cannot be blank', required=True)
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
            'new-user': data
        }


# login new user or admin
@namespace.route('/login', endpoint="Login")
class LoginUsers(Resource):
    """A view to authenticate all users"""
    email = None
    password = None
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('email', help='This field cannot be blank', required=True)
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
                ret = {'access_token': access_token}
                return jsonify(ret)

            elif admin is not False:
                access_token = create_access_token(identity=admin)
                ret = {'access_token': access_token}
                return jsonify(mes=ret)

            else:
                return jsonify(mes="None")



