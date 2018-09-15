from marshmallow import Schema, fields
import datetime as dt

from app.MenuItems.Models import MenuItem

orders = []


class Orders:
    """Orders Object"""

    def __init__(self):
        self.ID = None
        self.item = None
        self.quantity = None
        self.amount = None
        self.location = None
        self.owner = None
        self.created = None
        self.modified = None
        self.status = None
        MenuItem().create_sample_menu_items()

    @staticmethod
    def __set_id():
        """assign user id incrementaly"""
        number = len(orders)
        number = number + 1
        return number

    def create_order(self, item, quantity, location, owner=None):
        self.item = item
        self.quantity = quantity
        self.location = location
        self.owner = owner
        self.status = "Pending"
        self.item = self.__get_item(item)
        self.amount = self.__set_amount()
        self.created = dt.datetime.now()
        self.ID = self.__set_id()
        self.__set_amount()
        orders.append(self)
        return self

    @staticmethod
    def __get_item(item):
        it = MenuItem.get_specific_menu_item(item)
        if it is not False:
            return it
        else:
            raise FileNotFoundError("Menu Item not found")

    def __set_amount(self):
        self.amount = self.item.price * self.quantity
        return self.amount

    def set_quantity(self, qty):
        """modify the quantity"""
        self.quantity = qty
        self.__set_amount()

    @staticmethod
    def get_all_orders():
        return orders

    @staticmethod
    def get_order(order_id):
        for order in orders:
            if order.ID == order_id:
                return order
        return False

    def save_changes(self):
        it = self.get_order(self.ID)
        self.modified = dt.datetime.now()
        it = self
        return it

    def set_status(self, status):
        self.status = status
        self.save_changes()
        return self


class OrderSchema(Schema):
    ID = fields.Int()
    item = fields.Int()
    quantity = fields.Int()
    amount = fields.Float()
    status = fields.Str()
    owner = fields.Str()
    location = fields.Str()
    created = fields.Date()
    Modified = fields.Date()
