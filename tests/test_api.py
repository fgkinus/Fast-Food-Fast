import os

import pytest
from flask import Flask

from app import create_app, jwt
from app.Models import API


class TestAPI(object):
    def test_create_app(self):
        """test application factory"""
        app = create_app(__name__, 'testing')
        app2 = Flask(__name__)
        assert isinstance(app, type(app2))

    def test_type(self):
        """test api initialisation"""
        app = Flask(__name__)
        api = API(app, jwt)

        assert api is not None
        assert hasattr(api, 'app')

    def test_set_attr(self):
        """test attribute seeting function"""
        app = Flask(__name__)
        api = API(app, jwt, version='1.0', description='this')

        assert api.api.version == '1.0'
        assert api.api.description == 'this'

    def test_set_attribute_undefined(self):
        app = Flask(__name__)
        api = API(app, jwt)

        assert hasattr(api.app, 'not_exist') is False
        # test exception
        with pytest.raises(Exception, message="attribute not_exist not defined", ):
            api.set_attr(not_exist="unknown")
