from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource
from flask_restplus.reqparse import RequestParser

from app.MenuItems.Models import MenuItemSchema
from .Models import Orders, OrderSchema
from app.Accounts.decorators import *

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
        """fetch all orders"""
        orders = Orders().get_all_orders()

        # add items to the serialized output
        for order in orders:
            order.item = order.item.ID

        order_items = self.schema.dump(orders, many=True)
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

    # @admin_required
    @namespace.param(name='id', description="The identity of the order")
    def get(self, id):
        """get item"""
        schema = OrderSchema()

        item = Orders.get_order(int(id))
        if item is False:
            ret = {'message': 'item not found'}
            return ret, 200
        else:
            serialized = schema.dump(item)
            return serialized

    @namespace.param(name='id', description="modify the order")
    def patch(self, id):
        """get item"""
        schema = OrderSchema()

        item = Orders.get_order(int(id))
        if item is False:
            ret = {'message': 'item not found'}
            return ret, 200
        else:
            serialized = schema.dump(item)
            return serialized
