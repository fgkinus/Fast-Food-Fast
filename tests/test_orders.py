from app.MenuItems.Models import MenuItem
from app.Orders import Models
from tests.conftest import json_of_response


class TestOrders(object):
    def test_create_order(self):
        MenuItem().create_menu_item(name='name', price=500, image='', owner='me')
        length = len(Models.orders)
        Models.Orders().create_order(1, 3, 5)
        assert len(Models.orders) == length + 1

    def test_get_order(self):
        order = Models.Orders().get_order(1)

        assert isinstance(order, Models.Orders)
        assert order.ID is 1

    def test_get_all_orders(self):
        order = Models.Orders().get_all_orders()
        length = len(Models.orders)

        if length > 0:
            assert isinstance(order[length - 1], Models.Orders)
        assert length == len(order)

    def test_set_status(self):
        order = Models.Orders().create_order(item=1, quantity=2, location='juja', owner='test')
        assert order.status is "Pending"
        order.set_status('Canceled')
        assert order.status is "Canceled"

    def test_save_changes_to_orders(self):
        order = Models.Orders().get_order(1)
        order.set_quantity(5)
        order.save_changes()
        order = Models.Orders().get_order(1)
        assert order.quantity == 5
        assert order.amount == order.item.price * 5


class TestOrdersViews(object):
    """test the views associated with a orders"""

    def test_add_order(self, test_client, create_admin_token):
        # add test admin
        response = test_client.post('/api/v1/orders/', headers=create_admin_token,
                                    data=dict(
                                        item=1,
                                        quantity=2,
                                        location='Roysambu'
                                    ))
        json_data = json_of_response(response)
        assert response.status_code == 200

        assert len(json_data) == 2
        assert 'item' in json_data[1]

    def test_get_orders(self, test_client):
        """test get orders method"""
        pass
