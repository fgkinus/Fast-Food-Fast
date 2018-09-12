from app.MenuItems import Models


class TestMenuItems(object):
    def test_create_sample_menu_items(self):
        """clear the menu items list and  add samples"""
        # Models.menuitems.clear()
        Models.MenuItem().create_sample_menu_items()
        assert len(Models.menuitems) >= 3

    def test_create_menu_item(self):
        length = len(Models.menuitems)
        Models.MenuItem().create_menu_item('item', 'path', '200', 'test')
        assert length + 1 == len(Models.menuitems)

    def test_get_all_menu_items(self):
        items = Models.MenuItem().get_all_menu_items()
        length = len(Models.menuitems)
        assert len(items) == length

    def test_get_menu_item(self):
        Models.MenuItem().create_menu_item('item', 'path', '200', 'test')
        assert len(Models.menuitems) > 0
        item = Models.MenuItem().get_specific_menu_item(1)
        assert item.ID == 1
        Models.MenuItem().create_menu_item('item', 'path', '200', 'test')
        assert len(Models.menuitems) > 1
        item = Models.MenuItem().get_specific_menu_item(2)
        assert item.ID is 2
