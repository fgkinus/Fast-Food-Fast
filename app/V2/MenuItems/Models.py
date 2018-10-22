from flask_restplus import abort

from app.V1.MenuItems.Models import MenuItem as Base, MenuItemSchema
from app.V2 import DB


class MenuItems(Base):
    """a class definition for a menu Item"""

    def __init__(self):
        """initialize a menu item object"""
        self.schema = MenuItemSchema
        self.item = None

    def create_menu_item(self, details):
        """create a menu item """
        params = (
            details['name'],
            details['price'],
            details['owner']
        )
        item = DB.execute_procedures('add_menu_item', params)
        self.item = item[0]
        return self.item

    @staticmethod
    def get_specific_menu_item(id_no):
        """
        accept id_o return item
        :param id_no:
        :return: menuitem
        """
        item = DB.execute_procedures('get_menu_item_by_id', (id_no,))
        if len(item) == 0:
            abort(400, "The Menu Item was not found")
        else:
            return item[0]

    @staticmethod
    def get_all_menu_items():
        """Get all menu items"""
        item = DB.execute_procedures('get_menu_items')
        if len(item) == 0:
            abort(400, "There are no menu items to display!!!")
        else:
            return item

    @staticmethod
    def delete_menu_item(id_no):
        """
        remove and return a menu item
        :param id_no:
        :return:
        """
        item = DB.execute_procedures('delete_menu_item', (id_no,))
        if len(item) == 0:
            abort(400, "Menu Item not found")
        else:
            return item[0]

    @staticmethod
    def edit_menu_item(original, updated):
        """
        Accept the original and updated menu item details and update the database
        :param original:
        :param updated:
        :return: updated
        """
        item_id = original['id']

        details = (
            item_id,
            updated['name'],
            updated['price'],
            original['owner']
        )
        new_details = DB.execute_procedures('edit_menu_item', details)

        return new_details[0]

    def add_menuitem_image(self, item_id, image_url):
        """
        add an image url to the database for an item
        :param item_id:
        :param image_url:
        :return:
        """
        new_image = DB.execute_procedures('add_menu_item_image', (item_id, image_url))
        self.image = new_image[0]
        return self.image
