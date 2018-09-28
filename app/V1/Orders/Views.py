from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource
from flask_restplus.reqparse import RequestParser

from app.V1.MenuItems.Models import MenuItemSchema, MenuItem
from .Models import Orders, OrderSchema
from app.V1.Accounts.decorators import *

namespace = Namespace('Orders', description='Orders related operations')


@namespace.route('/', endpoint='Get-Order-items')
class ViewMenuOrders(Resource):
    """A viewset for Order items"""
    schema = OrderSchema()
    parser = RequestParser()
    parser.add_argument('item', required=True, type=int, help="item cannot be blank")
    parser.add_argument('quantity', required=True, type=int, help="item cannot be blank")
    parser.add_argument('location', required=True, type=str, help="item cannot be blank")
    parser.add_argument('owner', required=False, type=int)

    @jwt_required
    def get(self):
        """fetch all orders and create a copy"""
        orders = Orders().get_all_orders()
        temp = orders.copy()

        # add items to the serialized output
        for order in temp:
            if not isinstance(order.item, int):
                order.item = order.item.ID

        order_items = self.schema.dump(temp, many=True)
        return jsonify(order_items)

    @admin_required
    @namespace.expect(parser)
    def post(self):
        data = self.parser.parse_args()
        data['owner'] = get_jwt_identity()
        dump = self.schema.dump(data)

        # add now order to the orders
        dump = dump[0]
        order = Orders().create_order(dump['item'], dump['quantity'], dump['location'], dump['owner'])
        order_serialized = self.schema.dump(order)
        order_serialized[1]['item'] = MenuItemSchema().dump(order.item)
        return jsonify(order_serialized)


@namespace.route('/<id>', endpoint='get-a-specific-order-item ')
class ViewMenuOrderItem(Resource):
    """get specific ride detail"""
    parser = RequestParser()
    parser.add_argument('item', required=False, type=int, help="item cannot be blank")
    parser.add_argument('quantity', required=False, type=int, help="item cannot be blank")
    parser.add_argument('location', required=False, type=str, help="item cannot be blank")

    # parser.add_argument('owner', required=False, type=int)

    @admin_required
    @namespace.param(name='id', description="The identity of the order")
    def get(self, id):
        """get item"""
        schema = OrderSchema()

        item = Orders.get_order(int(id))

        serialized = schema.dump(item)
        return serialized

    @namespace.param(name='id', description="modify the order")
    @namespace.expect(parser)
    @admin_required
    def patch(self, id):
        """get item"""
        schema = OrderSchema()
        data = self.parser.parse_args()

        # check that item change has been done
        if isinstance(data['item'], int):
            data['item'] = MenuItem().get_specific_menu_item(data['item'])
        # get a menu item
        item = Orders.get_order(int(id))
        # register the changes
        item.register_changes(data)
        # serialize the input
        serialized = schema.dump(item)
        return serialized

    @namespace.param(name='id', description="Delete the Order")
    @jwt_required
    def delete(self, id):
        user = get_jwt_identity()
        item = Orders.get_order(int(id))
        if item.verify_owner(user):
            item.delete_order()
            return dict(message="Order Item deleted")


@namespace.route('/history', endpoint="get-historical-orders")
class HistoricalOrders(Resource):
    """View historical orders"""

    @jwt_required
    def get(self):
        """
        A method to display order history
        :return history:
        """
        user = get_jwt_identity()
        history = Orders().order_history(user)
        temp = history.copy()

        # add items to the serialized output
        for order in temp:
            if not isinstance(order.item, int):
                order.item = order.item.ID

        history_items = OrderSchema().dump(history, many=True)
        return history_items
