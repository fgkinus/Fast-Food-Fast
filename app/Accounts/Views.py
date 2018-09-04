from flask_restplus import Resource, reqparse, Namespace

# define a namespace for authentication and registration of users
from app.Accounts import Models

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
        user = Models.User().get_user(email=self.email, password=self.password) or Models.admin().get_user(
            email=self.email,
            password=self.password)

        if user is False:
            return {
                       'message': "wrong user or password"
                   }, 401
        else:
            return {
                       'welcome': data
                   }, 200
