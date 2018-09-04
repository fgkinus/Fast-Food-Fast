import pytest
from flask import Flask

from app.Models import API, Api


class TestAPI(object):
    def test_type(self):
        """test api initialisation"""
        app = Flask(__name__)
        api = API(app)

        assert api is not None
        assert hasattr(api, 'app')

    def test_set_attr(self):
        """test attribute seeting function"""
        app = Flask(__name__)
        api = API(app, version='1.0', description='this')

        assert api.api.version == '1.0'
        assert api.api.description == 'this'

    def test_set_attribute_undefined(self):
        app = Flask(__name__)
        api = API(app)

        assert hasattr(api.app, 'not_exist') is False
        # test exception
        with pytest.raises(Exception, message="attribute not_exist not defined", ):
            api.set_attr(not_exist="unknown")
