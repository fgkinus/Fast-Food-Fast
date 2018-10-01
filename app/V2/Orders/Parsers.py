from flask_restplus.reqparse import RequestParser


class Parsers:
    """a class instance of Order Parsers"""

    def __init__(self):
        self.raw = self.__raw_parser()
        self.detailed = None

    @staticmethod
    def __raw_parser():
        """create an instance of a raw Order details"""
        parser = RequestParser()
        parser.add_argument('item', required=True, type=int, help="the id of the item is required")
        parser.add_argument('quantity', required=True, type=int, help="the quantity of the item is required")
        parser.add_argument('owner', required=False, type=int, help="Please provide an image")
        parser.add_argument('location', required=True, help="Please provide a location for delivery")

        return parser
