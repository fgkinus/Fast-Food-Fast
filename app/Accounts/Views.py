from flask_restplus import Resource, reqparse, Namespace

# define a namespace for authentication and registration of users
from app.Accounts import Models

api = Namespace('Auth', description='user accounts related operations')


# register new user
class UserRegistration(Resource):
    request_parser = reqparse.RequestParser()
    username = None
    first_name = None
    second_name = None
    email = None
    password = None
    surname = None

    @api.route('/register-user', endpoint="add-new-user")
    def post(self):
        """add new admin user"""
        # initialise the request parser
        self.add_req_parsers()
        data = self.request_parser.parse_args()  # parse user input
        self.fetch_user_details(data=data)
        # create admin object
        user = Models.User(self.username, self.first_name, self.second_name, self.surname, self.password, self.email)

        return {
            'new-user': data
        }

    def add_req_parsers(self):
        self.reg_parser.add_argument('username', help='This field cannot be blank', required=True)
        self.reg_parser.add_argument('first_name', help='This field cannot be blank', required=True)
        self.reg_parser.add_argument('second_name', help='This field cannot be blank', required=True)
        self.reg_parser.add_argument('email', help='This field cannot be blank', required=True)
        self.reg_parser.add_argument('password', help='This field cannot be blank', required=True)
        self.reg_parser.add_argument('surname', help='This field cannot be blank', required=True)

    def fetch_user_details(self, data):
        """get parsed user details"""
        self.username = data['username']
        self.first_name = data['first_name']
        self.second_name = data['second_name']
        self.email = data['email']
        self.password = data['password']
        self.surname = data['surname']


# register new admin
class AdminRegistration(UserRegistration):
    """admin registration viewset"""

    @api.route('/register-admin', endpoint="add-new-admin")
    def post(self):
        """add new admin user"""
        # initialise the request parser
        self.add_req_parsers()
        data = self.request_parser.parse_args()  # parse user input
        self.fetch_user_details(data=data)
        # create admin object
        admin = Models.Admin(self.username, self.first_name, self.second_name, self.surname, self.password, self.email)

        return {
            'new-user': data
        }


# login new user or admin
class LoginUsers(Resource):
    """A view to authenticate all users"""
    email = None
    password = None

    def add_req_parsers(self):
        self.reg_parser.add_argument('email', help='This field cannot be blank', required=True)
        self.reg_parser.add_argument('password', help='This field cannot be blank', required=True)

    def fetch_user_details(self, data):
        """get parsed user details"""
        self.email = data['email']
        self.password = data['password']

    @api.route('login', endpoint="Login")
    def post(self):
        """add new admin user"""
        # initialise the request parser
        self.add_req_parsers()
        data = self.request_parser.parse_args()  # parse user input
        self.fetch_user_details(data=data)
        # search users
        user = Models.User.get_user(email=self.email, password=self.password) or Models.admin.get_user(email=self.email,
                                                                                                       password=self.password)

        return {
            'new-user': data
        }
