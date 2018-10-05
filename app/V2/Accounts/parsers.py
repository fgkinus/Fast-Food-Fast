from flask_restplus import reqparse, inputs
from flask_restplus.reqparse import RequestParser


class Parsers:
    """request parsers for the models"""

    def __init__(self):
        self.user = self.user_parser()
        self.login = self.login_details()

    @staticmethod
    def user_parser():
        """
        define and return a users parser
        :return: user_parser
        """
        request_parser = RequestParser(bundle_errors=True)
        request_parser.add_argument('username', required=True, help='Please provide the username')
        request_parser.add_argument('first_name', required=False)
        request_parser.add_argument('second_name', required=False)
        request_parser.add_argument('email', help='This field cannot be blank and should be a valid email address.',
                                    required=True,
                                    type=inputs.email())
        request_parser.add_argument('password', help='This field cannot be blank', required=True)
        request_parser.add_argument('surname', required=False)

        {
            "message": {
                "username": "The username argument should not be empty",
                "email": "This entry has to be a valid email address"
            }
        }

        return request_parser

    @staticmethod
    def login_details():
        """
        a parser for logging in details
        :return: parser
        """
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('email', help='Enter a valid user email here.', required=True,
                                    type=inputs.email())
        request_parser.add_argument('password', help='This field cannot be blank',
                                    required=True)
        return request_parser
