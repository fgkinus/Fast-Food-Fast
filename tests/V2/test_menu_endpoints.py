from app.urls import urls_v2, menu_ns_2
from tests.conftest import BaseTestClass


class TestMenuItems(BaseTestClass):
    """Test the menu Items endpoints"""

    def test_add_menu_item(self, test_client_2, create_admin_token):
        """add a new menu item"""
        response = test_client_2.post(urls_v2[menu_ns_2] + '/', data=self.item1,
                                      headers=create_admin_token)
        response2 = test_client_2.post(urls_v2[menu_ns_2] + '/', data=self.item2,
                                       headers=create_admin_token
                                       )
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)
        assert 'name' in response

    def test_get_menu_items(self, test_client_2):
        """list all  menu items"""
        response = test_client_2.get(urls_v2[menu_ns_2] + '/')
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, list)
        assert 'name' in response[0]

    def test_get_menu_item_id(self, test_client_2, create_user_token):
        """list all  menu items"""
        response = test_client_2.get(urls_v2[menu_ns_2] + '/1')
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)
        assert 'name' in response
        assert response['id'] == 1

    def test_non_numeric_parameter_in_get_menu_by_id(self, test_client_2, create_user_token):
        response = test_client_2.get(urls_v2[menu_ns_2] + '/l')
        assert response.status_code == 400
        response = self.json_of_response(response)
        assert isinstance(response, dict)
        assert 'message' in response

    def test_edit_menu_item(self, test_client_2, create_admin_token):
        """list all  menu items"""
        response = test_client_2.put(urls_v2[menu_ns_2] + '/1', headers=create_admin_token,
                                     data=self.item3
                                     )
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)
        assert 'details' in response
        assert response['details'][0]['price'] == 600
        assert response['details'][0]['name'] == 'test-item3'

    def test_delete_menu_item(self, test_client_2, create_admin_token):
        """list all  menu items"""
        response = test_client_2.delete(urls_v2[menu_ns_2] + '/1', headers=create_admin_token)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)

        response = test_client_2.get(urls_v2[menu_ns_2] + '/1')
        assert response.status_code == 400
        response = self.json_of_response(response)
        assert 'message' in response
