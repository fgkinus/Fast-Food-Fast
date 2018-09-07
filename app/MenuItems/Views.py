from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from flask_restplus.reqparse import RequestParser

from app.MenuItems.Models import MenuItem, MenuItemSchema
from .decorators import *


@namespace.route('/items', endpoint='Get-Menu-items')
class ViewMenuItems(Resource):
    """A viewset for menu items"""
    schema = MenuItemSchema()

    @jwt_required
    def get(self):
        MenuItem().create_menu_item(name='name', price=500, image='', owner='me')
        items = MenuItem().get_all_menu_items()
        serialized = MenuItemSchema().dump(items, many=True)

        return serialized


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
