from app.urls import urls_v2, orders_ns_2
from tests.conftest import BaseTestClass


class TestOrderResponses(BaseTestClass):
    """Test order responses"""

    def test_get_order_responses(self, test_client_2, create_admin_token):
        """test clients"""
        response = test_client_2.get(urls_v2[orders_ns_2] + '/response', headers=create_admin_token)
        assert response.status_code == 200
        response = self.json_of_response(response)
        assert isinstance(response, list)

    def test_add_order_response(self, test_client_2, create_admin_token):
        response = test_client_2.put(urls_v2[orders_ns_2] + '/2?response=2', headers=create_admin_token)
        assert response.status_code == 400
