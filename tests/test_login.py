from flask_jwt_extended import create_access_token

from app.Accounts import Models
from tests.conftest import json_of_response


class TestLogin(object):

    """Test case for user and admin users"""

    def test_user_login(self, test_client):
        # sample user
        user = Models.User().add_user(username='testuser', firstname='firstname', surname='sir', secondname='second',
                                      password='pass',
                                      email='test@test.com')
        response = test_client.post('/api/v1/login',
                                    data=dict(
                                        email='test@test.com',
                                        password='pass'
                                    ))

        assert response.status_code == 200

        json_data = json_of_response(response)
        if len(json_data) > 1:
            assert 'access_token' in json_data
            assert isinstance(json_data['details'], dict)

    def test_admin_login(self, test_client):
        # sample user
        user = Models.Admin().add_user(username='testadmin', firstname='firstname', surname='sir', secondname='second',
                                       password='pass',
                                       email='test@test.com')
        response = test_client.post('/api/v1/login',
                                    data=dict(
                                        email='test@test.com',
                                        password='pass'
                                    ))

        assert response.status_code == 200

        json_data = json_of_response(response)
        if len(json_data) > 1:
            assert 'access_token' in json_data
            assert isinstance(json_data['details'], dict)

    def test_wrong_user_credentials(self, test_client):
        response = test_client.post('/api/v1/login',
                                    data=dict(
                                        email='test@test.com',
                                        password='password'
                                    ))

        assert response.status_code == 401
