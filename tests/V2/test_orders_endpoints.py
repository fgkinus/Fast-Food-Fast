from app.urls import urls_v2, orders_ns_2
from tests.conftest import BaseTestClass


class TestOrders(BaseTestClass):
    """Test orders endpoints"""

    def test_add_order_unknown_item(self, test_client_2, create_user_token):
        """add an instance of a test order"""
        # its expected to fail if menu_item does not exist
        response = test_client_2.post(urls_v2[orders_ns_2] + '/', headers=create_user_token,
                                      data=self.order1)
        assert response.status_code == 500

    def test_add_order_known_item(self, test_client_2, create_user_token):
        """add an instance of a test order"""
        # # if the menu_item exists then its expected to pass
        response = test_client_2.post(urls_v2[orders_ns_2] + '/', headers=create_user_token,
                                      data=self.order2)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)
        assert response['quantity'] == 2
        assert response['item'] == 2

    def test_get_all_orders_non_admin_user(self, test_client_2, create_user_token):
        """list all orders in the database"""
        response = test_client_2.get(urls_v2[orders_ns_2] + '/', headers=create_user_token)
        assert response.status_code == 403

    def test_get_all_orders_admin_user(self, test_client_2, create_admin_token):
        """list all orders in the database"""
        response = test_client_2.get(urls_v2[orders_ns_2] + '/', headers=create_admin_token)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, list)

    def test_get_one_order_admin_user(self, test_client_2, create_admin_token):
        """get an order in the database"""
        response = test_client_2.get(urls_v2[orders_ns_2] + '/2', headers=create_admin_token)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)

    def test_get_order_history(self, test_client_2, create_user_token):
        """list all historical orders of authenticated user"""
        response = test_client_2.get(urls_v2[orders_ns_2] + '/history', headers=create_user_token)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, list)

    def test_edit_order_known_item_for_owner(self, test_client_2, create_user_token):
        """add an instance of a test order"""
        # # if the menu_item exists then its expected to pass
        response = test_client_2.patch(urls_v2[orders_ns_2] + '/2', headers=create_user_token,
                                       data=self.order3)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)
        assert 'modified' in response
        assert response['modified'][0]['quantity'] == 5
        assert response['modified'][0]['item'] == 2

    def test_edit_order_known_item_for_admin(self, test_client_2, create_admin_token):
        """add an instance of a test order"""
        # # if the menu_item exists then its expected to pass
        response = test_client_2.patch(urls_v2[orders_ns_2] + '/2', headers=create_admin_token,
                                       data=self.order4)
        assert response.status_code == 401

    def test_delete_order_known_item_for_owner(self, test_client_2, create_user_token):
        """add an instance of a test order"""
        # # if the menu_item exists then its expected to pass
        response = test_client_2.delete(urls_v2[orders_ns_2] + '/2', headers=create_user_token)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)
        assert 'item' in response
        assert response['item'][0]['quantity'] == 5
        assert response['item'][0]['item'] == 2
