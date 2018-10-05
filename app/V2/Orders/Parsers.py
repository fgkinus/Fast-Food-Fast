from flask_restplus.reqparse import RequestParser
from marshmallow import Schema, fields


class Parsers:
    """a class instance of Order Parsers"""

    def __init__(self):
        self.raw = self.__raw_parser()
        self.detailed = None
        self.response = self.__order_response_parser()

    @staticmethod
    def __raw_parser():
        """create an instance of a raw Order details"""
        parser = RequestParser()
        parser.add_argument('item', required=True, type=int, help="the id of the item is required",
                            )
        parser.add_argument('quantity', required=True, type=int, help="the quantity of the item is required")
        parser.add_argument('owner', required=False, type=int, help="The id of the owner")
        parser.add_argument('location', required=True, help="Please provide a location for delivery")

        return parser

    @staticmethod
    def __order_response_parser():
        """Create a parser for response identity"""
        parser = RequestParser()
        parser.add_argument('response', required=True, type=int, help="the id of the response is required")
        return parser


class ResponseSchema(Schema):
    """A schema class for response"""
    id = fields.Int(dump_only=True)
    order = fields.Int(dump_only=True)
    status = fields.Int(dump_only=True)
    owner = fields.Int(dump_only=True)
    created = fields.Date(dump_only=True)
    modified = fields.Date(dump_only=True)
