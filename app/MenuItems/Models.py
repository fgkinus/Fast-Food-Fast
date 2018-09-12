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


class MenuItemSchema(Schema):
    ID = fields.Int()
    name = fields.Str()
    image = fields.Str()
    price = fields.Float()
    owner = fields.Str()
    added = fields.Date()
    Modified = fields.Date()
