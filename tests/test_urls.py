from app.urls import urls, auth_ns


class TestURLs(object):
    """Test the api endpoints ie not 404"""

    def test_register_admin(self, test_client):
        """test the register_admin"""
        response = test_client.post(urls[auth_ns] + '/register-admin')
        assert response.status_code is not 404

    def test_register_user(self, test_client):
        """test the register_admin"""
        response = test_client.post(urls[auth_ns] + '/register-user')
        assert response.status_code is not 404

    def test_login(self, test_client):
        """test the register_admin"""
        response = test_client.post(urls[auth_ns] + '/login')
        assert response.status_code is not 404
