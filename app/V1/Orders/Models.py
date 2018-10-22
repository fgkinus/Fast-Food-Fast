from flask_restplus import abort
from marshmallow import Schema, fields
import datetime as dt

from app.V1.MenuItems.Models import MenuItem

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
        abort(204, "The specified order item does not Exist!!")

    def save_changes(self):
        it = self.get_order(self.ID)
        self.modified = dt.datetime.now()
        it = self
        return it

    def register_changes(self, changes):
        """register new changes and apply them"""
        for change in changes.keys():
            if changes[change] is not None:
                if hasattr(self, change):
                    setattr(self, change, changes[change])
            else:
                print("no changs")
        self.save_changes()

    def set_status(self, status):
        self.status = status
        self.save_changes()
        return self

    def verify_owner(self, username):
        if self.owner == username:
            return True
        else:
            print(self.owner)
            abort(401, "Unauthorised operation. You are not allowed to modify this order!!")

    def delete_order(self):
        """Get and remove order from list
        """
        order = self.get_order(self.ID)
        try:
            orders.remove(order)
        except Exception:
            abort(500, "Could not remove entry")

    @staticmethod
    def order_history(username):
        """
        display order history for a given user
        :param username:
        :return :history
        """
        history = list()
        for order in orders:
            if order.owner == username:
                history.append(order)
        if len(history) == 0:
            abort(204, "No historical orders available.please add more orders")
        return history


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    item = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda n: n > 0)
    amount = fields.Float()
    status = fields.String(dump_only=True)
    user = fields.Str(required=True)
    location = fields.Str(required=True)
    created = fields.Date()
    Modified = fields.Date()
