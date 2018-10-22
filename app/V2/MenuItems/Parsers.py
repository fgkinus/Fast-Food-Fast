from flask_restplus.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from app.V2.Accounts.parsers import Parsers as Base


class Parsers(Base):
    """request parsers for the models"""

    def __init__(self):
        self.item = self.item_parser()

    @staticmethod
    def item_parser():
        """parse menu item details"""
        parser = RequestParser()
        parser.add_argument('name', required=True, help="the name of the item is required")
        parser.add_argument('price', required=True, type=float, help="the price of the item is required")
        parser.add_argument('image', location='files', type=FileStorage, required=True)
        return parser
