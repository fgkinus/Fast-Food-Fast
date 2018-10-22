from flask_restplus import abort
from marshmallow import Schema, fields, ValidationError, validates
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
        """Create menu item"""

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

        abort(400, "item not found")

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
        """a method to delete a menu item from the list"""
        item = self.get_specific_menu_item(ID)
        if item is not False:
            menuitems.remove(item)
            return item
        return False

    def __set_attr(self, changes):
        # dynamically set class attributes
        for key in changes:
            if not hasattr(self, key):
                abort(400, "Attribute {0} not found".format(key))
            else:
                try:
                    setattr(self, key, changes[key])
                except AttributeError:
                    abort(400, "Attribute {0} could not be set".format(key))

    def save_changes(self, changes):
        """save changes to Menu item"""
        if isinstance(changes, dict):
            # set the attributes
            self.__set_attr(changes)
            # set the value for modified
            self.Modified = dt.datetime.now()

            # item = self.get_specific_menu_item(self.ID)
            # item = self


class MenuItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    image = fields.Url()
    price = fields.Float()
    owner = fields.Str(dump_only=True)
    added = fields.Date(dump_only=True)
    modified = fields.Date(dump_only=True)

    @validates('price')
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError('Quantity must be greater than 0.')
