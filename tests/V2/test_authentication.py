from app.urls import urls_v2, auth_ns_2
from tests.conftest import BaseTestClass


class TestAddUsers(BaseTestClass):
    """Test cases for user registration"""

    def test_add_user(self, test_client_2):
        response = test_client_2.post(urls_v2[auth_ns_2] + '/signup',
                                      data=self.user1)
        assert response.status_code == 200

    def test_add_admin(self, test_client_2, create_admin_token):
        response = test_client_2.post(urls_v2[auth_ns_2] + '/register-admin',
                                      data=self.admin1,
                                      headers=create_admin_token)
        assert response.status_code == 200


class TestAuth(BaseTestClass):
    """Test cases for use authentication"""

    def test_login(self, test_client_2):
        response = test_client_2.post(urls_v2[auth_ns_2] + '/login',
                                      data=dict(
                                          email=self.user1['email'],
                                          password=self.user1['password']
                                      ))

        assert response.status_code == 200
        response = self.json_of_response(response)

        assert 'details' in response
        assert 'access_token' in response

    def test_login_invalid_length_password(self, test_client_2):
        response = test_client_2.post(urls_v2[auth_ns_2] + '/login',
                                      data=dict(
                                          email='fgkinus@gmail.com',
                                          password='pass'
                                      ))

        assert response.status_code == 401

    def test_login_invalid_email(self, test_client_2):
        response = test_client_2.post(urls_v2[auth_ns_2] + '/login',
                                      data=dict(
                                          email='fgkinus',
                                          password='pass'
                                      ))

        assert response.status_code == 400


class TestGetUserProfile(BaseTestClass):
    """Fetch use profile of current user"""

    def test_get_user_profile(self, test_client_2, create_admin_token):
        response = test_client_2.get(urls_v2[auth_ns_2] + '/profile', headers=create_admin_token)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, dict)
        assert 'user_details' in response

    def test_edit_user_profile(self, test_client_2, create_admin_token):
        response = test_client_2.put(urls_v2[auth_ns_2] + '/profile', headers=create_admin_token, data=self.admin2)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert 'details' in response
        assert isinstance(response['details'], dict)
        assert response['details']['surname'] == 'surname'
