from flask_restplus import reqparse, inputs


class Parsers:
    """request parsers for the models"""

    def __init__(self):
        self.user = self.user_parser()

    @staticmethod
    def user_parser():
        """
        define and return a users parser
        :return: user_parser
        """
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('username', help='This field cannot be blank', required=True,)
        request_parser.add_argument('first_name', help='This field cannot be blank', required=True)
        request_parser.add_argument('second_name', help='This field cannot be blank', required=True)
        request_parser.add_argument('email', help='This field cannot be blank', required=True,
                                    type=inputs.email(check=True))
        request_parser.add_argument('password', help='This field cannot be blank', required=True)
        request_parser.add_argument('surname', help='This field cannot be blank', required=True)
        return request_parser
