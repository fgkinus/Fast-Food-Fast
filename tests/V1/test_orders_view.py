from tests.V1.conftest import json_of_response


class TestOrdersViews(object):
    """test the views associated with a orders"""

    def test_add_order(self, test_client, create_admin_token):
        # add test admin
        response = test_client.post('/api/v1/orders/', headers=create_admin_token,
                                    data=dict(
                                        item=1,
                                        quantity=2,
                                        location='Roysambu'
                                    ))
        json_data = json_of_response(response)
        assert response.status_code == 200

        assert len(json_data) == 2
        assert 'item' in json_data[1]

    def test_get_orders(self, test_client):
        """test get orders method"""
        pass
