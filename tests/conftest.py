import json
import os

import pytest

from app import create_app, jwt
from app.Models import API, URLS
from app.urls import urls


@pytest.fixture
def test_client():
    app = create_app(__name__, 'testing')
    app.config['JWT_SECRET_KEY'] = app.config['SECRET']
    api = API(app, jwt)
    api = URLS(api, urls=urls).get_api()

    client = api.app.test_client()
    ctx = api.app.app_context()
    ctx.push()
    yield client
    ctx.pop()


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))
