from marshmallow import Schema, fields
import datetime as dt

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
        self.ID = self.__set_id()

    def get_menu_item(self):
        return self

    @staticmethod
    def get_all_menu_items():
        return menuitems

    @staticmethod
    def get_specific_menu_item(id_no):
        for item in menuitems:
            if item.ID == id_no:
                return item

        return False

    def __set_id(self):
        """assign user id incrementaly"""
        number = len(menuitems)
        number = number + 1
        menuitems.append(self)
        return number


class MenuItemSchema(Schema):
    ID = fields.Int()
    name = fields.Str()
    image = fields.Str()
    price = fields.Float()
    owner = fields.Str()
    added = fields.Date()
    Modified = fields.Date()
