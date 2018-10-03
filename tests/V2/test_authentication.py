from app.urls import urls_v2, auth_ns_2
from tests.conftest import json_of_response


class TestAddUsers(object):
    """Test cases for user registration"""

    def test_add_user(self, test_client_2):
        response = test_client_2.post(urls_v2[auth_ns_2] + '/signup',
                                      data=dict(
                                          email='fgkinus@gmail.com',
                                          password='password',
                                          username='fgtash',
                                          surname='fgtash',
                                          first_name='first',
                                          second_name='second'
                                      ))
        assert response.status_code == 200

    def test_add_admin(self, test_client_2, create_admin_token):
        response = test_client_2.post(urls_v2[auth_ns_2] + '/register-admin',
                                      data=dict(
                                          email='testadmin@gmail.com',
                                          password='password',
                                          username='testadmin',
                                          surname='fgtash',
                                          first_name='first',
                                          second_name='second'
                                      ),
                                      headers=create_admin_token)
        assert response.status_code == 200


class TestAuth(object):
    """Test cases for use authentication"""

    def test_login(self, test_client_2):
        response = test_client_2.post(urls_v2[auth_ns_2] + '/login',
                                      data=dict(
                                          email='fgkinus@gmail.com',
                                          password='password'
                                      ))

        assert response.status_code == 200
        response = json_of_response(response)

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


class TestGetUserProfile(object):
    """Fetch use profile of current user"""

    def test_get_user_profile(self, test_client_2, create_admin_token):
        response = test_client_2.get(urls_v2[auth_ns_2] + '/profile', headers=create_admin_token)
        assert response.status_code == 200
        response = json_of_response(response)
        assert isinstance(response, dict)
        assert 'user_details' in response

    def test_edit_user_profile(self, test_client_2, create_admin_token):
        response = test_client_2.put(urls_v2[auth_ns_2] + '/profile', headers=create_admin_token, data=dict(
            email='testadmin2@gmail.com',
            password='password',
            username='new-test-user',
            surname='surname',
            first_name='first',
            second_name='second'))
        assert response.status_code == 200
        response = json_of_response(response)
        assert 'details' in response
        assert isinstance(response['details'], list)
        assert response['details'][0]['surname'] == 'surname'
