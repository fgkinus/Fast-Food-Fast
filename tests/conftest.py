import json

import pytest
import sys
from flask_jwt_extended import create_access_token

from app import create_app, jwt
from app.V1.Accounts.Models import Admin, User
from app.Models import API, URLS
from app.V2 import DB
from app.V2.Accounts.Models import User
from app.urls import urls_v1, urls_v2


# CREATE TESTS
# ADMIN = Admin().add_user(username='testadmin', firstname='firstname', surname='sir', secondname='second',
#                          password='pass',
#                          email='test@test.com')
# # USER = User().add_user(username='testuser', firstname='firstname', surname='sir', secondname='second',
#                        password='pass',
#                        email='test@test.com')


def tear_down_db():
    try:
        DB.query_db("DROP SCHEMA public CASCADE;CREATE SCHEMA IF NOT EXISTS public;")
    except:
        print("Error: ", sys.exc_info()[1])


@pytest.fixture(scope='session')
def test_client():
    """A fixture to yield the test client"""
    app = create_app(__name__, 'testing')
    app.config['JWT_SECRET_KEY'] = app.config['SECRET']
    api = API(app, jwt)
    api = URLS(api, urls=urls_v1).get_api()

    client = api.app.test_client()
    ctx = api.app.app_context()
    ctx.push()
    yield client
    ctx.pop()


@pytest.fixture(scope='session')
def test_client_2():
    """A fixture to yield the test client"""
    app = create_app(__name__, 'testing')
    app.config['JWT_SECRET_KEY'] = app.config['SECRET']
    api = API(app, jwt)
    api = URLS(api, urls=urls_v2).get_api()

    client = api.app.test_client()
    ctx = api.app.app_context()
    ctx.push()
    yield client
    ctx.pop()
    tear_down_db()


@pytest.fixture()
def create_admin_token():
    "a reusable function to create an admin token"
    user = User().login_user('admin@email.com', 'password')
    # create access token
    access_token_admin = create_access_token(identity=user)
    # create header
    header_admin = {
        'Authorization': 'Bearer {}'.format(access_token_admin)
    }
    return header_admin


@pytest.fixture()
def create_user_token():
    """A reusable function to create a user token"""
    user = User().login_user('kinusfg@email.com', 'password')
    # create access token
    access_token_user = create_access_token(identity=user)
    # create header
    header_user = {
        'Authorization': 'Bearer {}'.format(access_token_user)
    }
    return header_user


@pytest.fixture()
def create_admin_token_v1():
    "a reusable function to create an admin token"
    user = User().login_user('admin@email.com', 'password')
    # create access token
    access_token_admin = create_access_token(identity=user)
    # create header
    header_admin = {
        'Authorization': 'Bearer {}'.format(access_token_admin)
    }
    return header_admin


@pytest.fixture()
def create_user_token_v1():
    """A reusable function to create a user token"""
    user = User().login_user('kinusfg@email.com', 'password')
    # create access token
    access_token_user = create_access_token(identity=user)
    # create header
    header_user = {
        'Authorization': 'Bearer {}'.format(access_token_user)
    }
    return header_user


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))
