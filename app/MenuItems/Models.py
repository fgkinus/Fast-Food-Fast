from flask_restplus import abort
from marshmallow import Schema, fields
import datetime as dt

from app.Exceptions import AlreadyExists

menuitems = []


class MenuItem:
    """"Menu item model"""

    def __init__(self):
        self.ID = None
        self.name = None
        self.image = None
        self.price = None
        self.owner = None
        self.added = None
        self.Modified = None

    def create_menu_item(self, name, image, price, owner):
        """CReate menu item"""

        self.name = name
        self.image = image
        self.price = price
        self.owner = owner
        self.added = dt.datetime.now()
        self.check_already_exists()
        self.ID = self.__set_id()
        return self

    def get_menu_item(self):
        return self

    @staticmethod
    def get_all_menu_items():
        return menuitems

    @staticmethod
    def get_specific_menu_item(id_no):
        """verify item id number exist iteratively else false"""
        for item in menuitems:
            # print(item.ID)
            if item.ID == id_no:
                return item

        return False

    def __set_id(self):
        """assign user id incrementaly"""
        number = len(menuitems)
        number = number + 1
        menuitems.append(self)
        return number

    @staticmethod
    def create_sample_menu_items():
        if len(menuitems) < 1:
            MenuItem().create_menu_item('fries', './images/fries.jpg', 200, 'sys')
            MenuItem().create_menu_item('burger', './images/burger.jpg', 300, 'sys')
            MenuItem().create_menu_item('sandwich', './images/sandwich.jpg', 600, 'sys')

    def check_already_exists(self):
        """Check if name already exists and throw exception"""
        for item in menuitems:
            if self.name == item.name:
                abort(400, "The item you tried to add already exists")
                raise AlreadyExists("The item you tried to add already exists")

    def delete_menu_item(self, ID):
        item = self.get_specific_menu_item(ID)
        if item is not False:
            menuitems.remove(item)
            return item
        return False


class MenuItemSchema(Schema):
    ID = fields.Int()
    name = fields.Str()
    image = fields.Str()
    price = fields.Float()
    owner = fields.Str()
    added = fields.Date()
    Modified = fields.Date()
