from flask_jwt_extended import jwt_required
from flask_restful import marshal_with
from flask_restplus import Resource
from flask_restplus.reqparse import RequestParser

from app.MenuItems.Models import MenuItem, MenuItemSchema
from .decorators import *


@namespace.route('/orders', endpoint='Get Order items')
class ViewMenuOrders(Resource):
    """A viewset for Order items"""
    schema = MenuItemSchema()
