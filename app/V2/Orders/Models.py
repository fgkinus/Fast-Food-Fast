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
        DB.logger.debug(self.details)
        return self

    def get_order(self, order_id):
        """
        Fetch and return an Order item
        :return: Order
        """
        if self.details is None:
            order = DB.execute_procedures('get_order_item_by_id', (order_id,))
            DB.logger.debug(order)
            self.details = order[0]
            # now update the order status
            st = dict(
                status=self.get_order_status(self.details['id'])
            )
            self.details.update(st)

            # return the response
            return self.details
        else:
            return self.details

    def get_all_orders(self):
        """
        returns a list of all orders in the DB
        :return:
        """
        orders = DB.execute_procedures('get_order_items', ())
        if len(orders) == 0:
            abort(400, "There are no orders to display")

        # set order status
        for order in orders:
            st = dict(
                status=self.get_order_status(order_id=order['id'])
            )
            order.update(st)

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
        if len(history) == 0:
            abort(400, "There is no order History to display")
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
        status = DB.execute_procedures('get_all_order_status', ())
        status = status
        return status

    def check_order_statuses_exist(self, status_id):
        """
        Get order status if exists
        :return status_details:
        """
        status = self.get_order_statuses()
        for st in status:
            if st['id'] == status_id:
                return st
        abort(400, "The status id does not reference a known response ")

    def set_order_status(self, order, response, owner):
        """
        Add response for orders
        :param order:
        :param response:
        :param owner:
        :return:
        """
        # response = DB.query_db_with_results(
        #     "SELECT * from set_order_status({0},{1},{2})".format(order, response, owner))
        response = DB.execute_procedures('set_order_status', (order, response, owner))
        self.status = response[0]
        self.details['status'] = self.status['status']
        return self.details

    def edit_order_status(self, order, response, owner):
        """
        Add response for orders
        :param order:
        :param response:
        :param owner:
        :return:
        """
        # response = DB.query_db_with_results(
        #     "SELECT * from set_order_status({0},{1},{2})".format(order, response, owner))
        response = DB.execute_procedures('edit_order_status', (order, response, owner))
        self.status = response[0]
        self.details['status'] = response[0]['status']
        return self.details

    def get_order_status(self, order_id):
        """
        get the order status for a specific order
        :param order_id:
        :return:
        """
        response = DB.execute_procedures('get_order_status', (order_id,))
        if len(response) == 0:
            return 'New'
        self.status = response[0]['description']
        return self.status
