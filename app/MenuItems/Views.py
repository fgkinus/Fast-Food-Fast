from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource
from flask_restplus.reqparse import RequestParser

from app.ExceptionHandlers import ExceptionHandler
from app.MenuItems.Models import MenuItem, MenuItemSchema
from .decorators import *

parser = RequestParser()
parser.add_argument('name', required=True, help="the name of the item is required")
parser.add_argument('price', required=True, help="the name of the item is required")
parser.add_argument('image', required=False, help="Please provide an image")


@namespace.route('/items', endpoint='Get-Menu-items')
class ViewMenuItems(Resource):
    """A viewset for menu items"""
    schema = MenuItemSchema()

    @jwt_required
    def get(self):
        MenuItem().create_sample_menu_items()
        items = MenuItem().get_all_menu_items()
        serialized = MenuItemSchema().dump(items, many=True)

        return serialized

    @admin_required
    def post(self):
        """add item only if you are an admin"""
        data = parser.parse_args()
        owner = get_jwt_identity()
        item = MenuItem().create_menu_item(data['name'], data['image'], data['price'], owner)
        dump = self.schema.dump(item)
        mes = dict(
            message="item  added",
            item=dump
        )
        return mes, 201


@namespace.route('/items/<id>', endpoint='get-a-specific-menu-item ')
class ViewMenuItem(Resource):
    """get specific ride detail"""

    @jwt_required
    @namespace.param(name='id', description="The identity of te menu item")
    def get(self, id):
        """get item"""

        item = MenuItem().get_specific_menu_item(int(id))
        if item is False:
            ret = {'message': 'item not found'}
            return ret, 200
        else:
            serialized = MenuItemSchema().dump(item)
            return serialized
