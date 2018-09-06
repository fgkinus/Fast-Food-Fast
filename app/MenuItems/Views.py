from flask_jwt_extended import jwt_required
from flask_restful import marshal_with
from flask_restplus import Resource
from flask_restplus.reqparse import RequestParser

from app.MenuItems.Models import MenuItem, MenuItemSchema
from .decorators import *


@namespace.route('/items', endpoint='Get Menu items')
class ViewMenuItems(Resource):
    """A viewset for menu items"""
    schema = MenuItemSchema()

    @jwt_required
    def get(self):
        MenuItem().create_menu_item(name='name', price=500, image='', owner='me')
        items = MenuItem().get_all_menu_items()
        serialized = MenuItemSchema().dump(items, many=True)

        ret = {'items': serialized}
        return serialized
