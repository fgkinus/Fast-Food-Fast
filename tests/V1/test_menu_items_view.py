from flask_jwt_extended import get_jwt_identity

from app.V1.MenuItems.Models import menuitems
from app.urls import urls, menu_ns
from tests.V1.conftest import json_of_response


class TestMenuItemsView(object):
    """Test the views for menu items"""

    def test_get_menu_items(self, test_client, create_admin_token):
        """test get all menu items"""
        response = test_client.get(urls[menu_ns] + '/items', headers=create_admin_token)

        assert response.status_code == 200
        response = json_of_response(response)
        assert isinstance(response, list)

    def test_get_menu_item(self, test_client, create_admin_token):
        """test get a menu item"""
        response = test_client.get(urls[menu_ns] + '/items/3', headers=create_admin_token)

        assert response.status_code == 200
        response = json_of_response(response)
        assert 'ID' in response

    def test_add_menu_item(self, test_client, create_admin_token):
        """test add  menu items"""
        response = test_client.post(urls[menu_ns] + '/items', headers=create_admin_token,
                                    data=dict(
                                        name='food-item',
                                        price=300,
                                        path='path',
                                        owner=get_jwt_identity()
                                    ))

        assert response.status_code == 201
        response = json_of_response(response)
        assert 'item' in response
        assert isinstance(response['item'], list)

    def test_add_duplicate_menu_item(self, test_client, create_admin_token):
        """test add  menu items"""
        response = test_client.post(urls[menu_ns] + '/items', headers=create_admin_token,
                                    data=dict(
                                        name='food-item',
                                        price=300,
                                        path='path',
                                        owner=get_jwt_identity()
                                    ))

        assert response.status_code == 400
        response = json_of_response(response)
        assert 'message' in response
        assert isinstance(response, dict)

    def test_removal_of_menu_item(self, test_client, create_admin_token):
        """remove a menu item"""
        ID = len(menuitems)
        response = test_client.delete(urls[menu_ns] + '/items/{0}'.format(ID), headers=create_admin_token)
        assert response.status_code == 400
