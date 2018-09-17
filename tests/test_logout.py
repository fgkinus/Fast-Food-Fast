from app.Accounts.Models import blacklist
from app.urls import urls, auth_ns


class TestLogout(object):
    """test cases for log out"""

    def test_logout_request_for_admin(self, test_client, create_admin_token):
        response = test_client.post(urls[auth_ns] + '/logout', headers=create_admin_token)
        assert response.status_code == 200
        assert len(blacklist) > 0

    def test_logout_request_for_user(self, test_client, create_user_token):
        response = test_client.post(urls[auth_ns] + '/logout', headers=create_user_token)
        assert response.status_code == 200
        assert len(blacklist) > 1
