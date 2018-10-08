from app.urls import urls_v1, order_ns, menu_ns, auth_ns


class TestURLs(object):
    """Test the API endpoints ie not 404"""

    def test_register_admin(self, test_client):
        """test the register_admin"""
        response = test_client.post(urls_v1[auth_ns] + '/register-admin')
        assert response.status_code is not 404

    def test_register_user(self, test_client):
        """test the register_admin"""
        response = test_client.post(urls_v1[auth_ns] + '/register-user')
        assert response.status_code is not 404

    def test_login(self, test_client):
        """test the register_admin"""
        response = test_client.post(urls_v1[auth_ns] + '/login')
        assert response.status_code is not 404

    def test_get_menu(self, test_client):
        """test the register_admin"""
        response = test_client.get(urls_v1[menu_ns] + '/items')
        assert response.status_code is not 404

    def test_get_a_menu_item(self, test_client):
        """test the register_admin"""
        response = test_client.get(urls_v1[menu_ns] + '/items/1')
        assert response.status_code is not 404

    def test_get_an_order_item(self, test_client):
        """test the register_admin"""
        response = test_client.get(urls_v1[order_ns] + '/order/1')
        assert response.status_code is not 404
