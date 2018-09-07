from flask_jwt_extended import jwt_required
from flask_restful import marshal_with
from flask_restplus import Resource
from flask_restplus.reqparse import RequestParser

from .Models import Orders, OrderSchema
from .decorators import *


@namespace.route('/', endpoint='Get-Order-items')
class ViewMenuOrderss(Resource):
    """A viewset for Order items"""
    schema = OrderSchema()
    parser = RequestParser()

    @admin_required
    def get(self):
        orders = Orders().get_all_orders()
        order_items = self.schema.dump(orders, many=True)
        return order_items

    # @admin_required
    @namespace.expect(schema)
    def post(self):
        data = self.parser.parse_args()
        orders = Orders().get_all_orders()
        order_items = self.schema.dump(orders, many=True)
        return order_items


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
