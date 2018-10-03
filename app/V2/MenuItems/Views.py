from flask_jwt_extended import get_jwt_identity
from flask_restplus import Resource
from marshmallow import ValidationError

from app.V2 import DB
from app.V2.Accounts.Models import User
from app.V2.MenuItems.Models import MenuItems
from app.V2.MenuItems.Parsers import Parsers
from app.V2.decorators import *
from app.V2.utils import Utils

namespace = Namespace("MenuItems", "Menu Items Related Operations")


@namespace.route('/', endpoint="add-edit menu items")
class ViewAddMenuItems(Resource):
    """add and view menu items"""

    @admin_required
    @namespace.expect(Parsers().item)
    def post(self):
        """
        add a new menu item if admin
        :return: MenuItem
        """
        user = get_jwt_identity()
        user_details = User().get_user_by_username(user)
        data = Parsers().item.parse_args()
        data.update({'owner': user_details['id']})

        try:
            MenuItems().schema().load(data)
        except ValidationError as error:
            DB.logger.error(str(error))
            return {'message': str(error)}, getattr(error, 'code', 401)
        item = MenuItems().create_menu_item(data)

        return MenuItems().schema().dump(item)

    def get(self):
        """
        list all menu items
        :return:
        """
        items = MenuItems().get_all_menu_items()
        items = MenuItems().schema().dump(items, many=True)
        return items


@namespace.route('/<item_id>', endpoint="add-edit menuitem")
class ViewEditMenuItems(Resource):
    """Views for editting and modifying menu items"""

    def get(self, item_id):
        """
        get a specific menu item
        :param item_id:
        :return:
        """
        item_id = Utils.parse_int(item_id)
        items = MenuItems().get_specific_menu_item(item_id)
        item = MenuItems().schema().dump(items)

        return item

    @admin_required
    def delete(self, item_id):
        """
        remove and return menu item
        :param item_id:
        :return:
        """
        item_id = Utils.parse_int(item_id)
        items = MenuItems().delete_menu_item(item_id)
        item = MenuItems().schema().dump(items)
        ret = dict(
            message="Item Deleted",
            details=item
        )
        return ret

    @admin_required
    @namespace.expect(Parsers().item)
    def put(self, item_id):
        """
        edit a menu items details
        :return: modified
        """
        item_id = Utils.parse_int(item_id)
        data = Parsers().item.parse_args()
        original = MenuItems().get_specific_menu_item(item_id)
        modified = MenuItems().edit_menu_item(original, data)
        modified = MenuItems().schema().dump(modified)

        ret = dict(
            message="Menu-item Modified",
            details=modified
        )

        return ret
