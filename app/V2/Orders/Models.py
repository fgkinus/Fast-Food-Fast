from flask_restplus import abort

from app.V1.Orders.Models import Orders as Base, OrderSchema
from app.V2 import DB
from app.V2.Accounts.Models import User


class Order(Base):
    """A class representing an order instance"""

    def __init__(self):
        """Initialise an order item"""
        self.details = None
        self.parser = OrderSchema

    def create_order(self, item, quantity, location, owner):
        """
        add a new Order Item
        :param item:
        :param quantity:
        :param location:
        :param owner:
        :return: Order
        """
        order = DB.execute_procedures('add_order_item', (item, quantity, location, owner))
        self.details = order[0]
        return self

    def get_order(self, order_id):
        """
        Fetch and return an Order item
        :return: Order
        """
        if self.details is None:
            order = DB.execute_procedures('get_order_item_by_id', (order_id,))
            self.details = order[0]
            return self.details
        else:
            return self.details

    @staticmethod
    def get_all_orders():
        """
        returns a list of all orders in the DB
        :return:
        """
        orders = DB.execute_procedures('get_order_items', ())
        return orders

    def delete_order(self, order_id):
        """
        A  method to delete order items
        :return: Deleted_item
        """
        order = DB.execute_procedures('delete_order_item', (order_id,))
        self.details = order[0]
        return self.details

    def modify_order(self, order_id, item, quantity, location, owner):
        """
        get order and update it details
        :param order_id:
        :param item:
        :param quantity:
        :param location:
        :param owner:
        :return: modified
        """
        modified = DB.execute_procedures('edit_order_item', (order_id, item, quantity, location, owner))
        self.details = modified[0]
        return self.details

    @staticmethod
    def get_historical_orders(user):
        """
        get and return a specific users historical orders
        :param user:
        :return: history
        """
        history = DB.execute_procedures('get_order_item_by_user_id', (user,))
        return history

    def verify_owner(self, username):
        """
        verify te owner of the order or raise 401
        :param username:
        :return: bool
        """
        user = User().get_user_by_username(username)

        if self.details['user'] != user['id']:
            abort(401, "You are not authorised a to modify this order")

        else:
            return True

    @staticmethod
    def get_order_statuses():
        """
        Get and return all order statuses
        :return: order statuses
        """
        pass

    @staticmethod
    def check_order_statuses_exist(status_id):
        """
        Get order status exists
        :return status_details:
        """
        pass
