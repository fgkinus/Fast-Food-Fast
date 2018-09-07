from app.MenuItems.Models import MenuItem
from app.Orders import Models


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
