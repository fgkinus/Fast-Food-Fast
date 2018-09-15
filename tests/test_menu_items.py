import pytest
from werkzeug.exceptions import BadRequest

from app.Exceptions import AlreadyExists
from app.MenuItems import Models


class TestMenuItems(object):
    def test_create_sample_menu_items(self):
        """clear the menu items list and  add samples"""
        # Models.menuitems.clear()
        Models.MenuItem().create_sample_menu_items()
        assert len(Models.menuitems) >= 3

    def test_create_menu_item(self):
        length = len(Models.menuitems)
        Models.MenuItem().create_menu_item('item1', 'path', '200', 'test')
        assert length + 1 == len(Models.menuitems)

    def test_get_all_menu_items(self):
        items = Models.MenuItem().get_all_menu_items()
        length = len(Models.menuitems)
        assert len(items) == length

    def test_get_menu_item(self):
        Models.MenuItem().create_menu_item('item2', 'path', '200', 'test')
        assert len(Models.menuitems) > 0
        item = Models.MenuItem().get_specific_menu_item(1)
        assert item.ID == 1
        Models.MenuItem().create_menu_item('item3', 'path', '200', 'test')
        assert len(Models.menuitems) > 1
        item = Models.MenuItem().get_specific_menu_item(2)
        assert item.ID is 2

    def test_already_exists(self):
        """add a menu item and add it again to catch exception"""
        Models.MenuItem().create_menu_item('unique_item', 'path', '200', 'test')
        with pytest.raises(BadRequest, message="The item you tried to add already exists"):
            Models.MenuItem().create_menu_item('unique_item', 'path', '200', 'test')
