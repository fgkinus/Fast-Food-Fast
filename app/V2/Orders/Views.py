from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, Namespace, abort

from app.V2.Accounts.Models import User
from app.V2.Orders import Parsers
from app.V2.Orders.Models import Order
from app.V2.Orders.Parsers import Parsers
from app.V2.decorators import admin_required
from app.V2.utils import Utils

namespace = Namespace("Orders", "Order Related Operations", decorators=[jwt_required])


@namespace.doc("add new orders")
@namespace.route('/')
class AddListOrders(Resource):
    """Add orders"""

    @jwt_required
    @namespace.expect(Parsers().raw)
    def post(self):
        """
        add a new order item to the DB.
        :return: new_order
        """
        user = get_jwt_identity()
        user = User().get_user_by_username(username=user)
        data = Parsers().raw.parse_args()
        order = Order().create_order(data['item'], data['quantity'], data['location'], user['id'])
        order = Order().parser().dump(order.details)

        return order

    @admin_required
    @namespace.doc("list all orders")
    def get(self):
        """List all order items"""
        orders = Order().get_all_orders()
        orders = Order().parser().dump(orders, many=True)
        return orders


@namespace.route('/history', endpoint='display-order history')
class GetOrderHistory(Resource):
    """Fetch the authenticated users order history"""

    @jwt_required
    @namespace.doc("List all historical personal orders")
    def get(self):
        """fetch and list all historical orders"""
        user = get_jwt_identity()
        user = User().get_user_by_username(username=user)
        history = Order().get_historical_orders(user=user['id'])
        serialized = Order().parser().dump(history, many=True)
        return serialized


@namespace.route('/<order_id>')
class GetEditDeleteOrder(Resource):
    """Get edit or delete Order detail"""

    @jwt_required
    def get(self, order_id):
        """Fetch a specific order"""
        order_id = Utils.parse_int(order_id)
        order = Order().get_order(order_id)
        serialized = Order().parser().dump(order)
        return serialized

    @jwt_required
    def delete(self, order_id):
        """delete an order if you own it"""
        order_id = Utils.parse_int(order_id)
        order = Order()
        order.get_order(order_id)
        order.verify_owner(get_jwt_identity())
        deleted = order.delete_order(order_id)
        serialized = order.parser().dump(deleted)
        # now validate the user
        ret = {
            "message": "The item has been deleted",
            "item": serialized
        }

        return ret

    @jwt_required
    @namespace.expect(Parsers().raw)
    def put(self, order_id):
        """Edit an order"""
        order_id = Utils.parse_int(order_id)
        order = Order()
        order.get_order(order_id)
        order.verify_owner(get_jwt_identity())

        data = Parsers().raw.parse_args()
        order.modify_order(order_id, item=data['item'], quantity=data['quantity'], location=data['location'],
                           owner=order.details['user'])
        ret = dict(
            message="The order item has been modified",
            modified=order.parser().dump(order.details)
        )

        return ret


@namespace.route('/response/<order_id>/<response>')
class OrderRespose:
    """Add and Edit order responses for admin"""

    def post(self, order_id, response):
        """add order response"""
        pass
