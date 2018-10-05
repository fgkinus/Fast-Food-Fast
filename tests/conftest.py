import json

import pytest
import sys
from flask_jwt_extended import create_access_token

from app import create_app, jwt
from app.Models import API, URLS
from app.V2 import DB, Database, connection
from app.V2.Accounts.Models import User
from app.urls import urls_v1, urls_v2


class BaseTestClass(object):
    """contains the Base test variables"""

    user1 = dict(
        email='fg@gmail.com',
        password='password',
        username='test_user',
        surname='fgtash',
        first_name='first',
        second_name='second'
    )

    user3 = dict(
        email='fg@gmail.com',
        password='password',
        username='test_user',
        first_name='first',
        second_name='second'
    )
    admin3 = dict(
        email='fg@gmail.com',
        password='password',
        username='test_user',
        first_name='first',
        second_name='second'
    )

    base_user = dict(
        email='kinusfg@email.com',
        password='password',
        username='fgkinus',
        surname='fgtash',
        first_name='first',
        second_name='second'
    )

    admin1 = dict(
        email='testadmin@gmail.com',
        password='password',
        username='testadmin',
        surname='fgtash',
        first_name='first',
        second_name='second'
    )

    base_admin = dict(
        email='admin@email.com',
        password='password',
        username='admin',
        surname='fgtash',
        first_name='first',
        second_name='second'
    )
    admin2 = dict(
        email='testadmin2@gmail.com',
        password='password',
        username='new-test-user',
        surname='surname',
        first_name='first',
        second_name='second')

    item1 = dict(
        name='test_item',
        price=500
    )

    item2 = dict(
        name='test_item2',
        price=500
    )

    item3 = dict(
        name='test-item3',
        price=600
    )

    order1 = dict(
        item=1,
        quantity=2,
        location='nowhere'
    )

    order2 = dict(
        item=2,
        quantity=2,
        location='nowhere'
    )
    order3 = dict(
        item=2,
        quantity=5,
        location='nowhere'
    )
    order4 = dict(
        item=2,
        quantity=5,
        location='nowhere'
    )

    @staticmethod
    def json_of_response(response):
        """Decode json from response"""
        return json.loads(response.data.decode('utf8'))

    def create_base_test_user(self):
        new = User().add_admin(self.base_admin)
        return new

    def create_base_test_admin(self):
        new = User().add_admin(self.base_user)
        return new


def tear_down_db():
    try:
        DB.query_db("DROP SCHEMA public CASCADE;CREATE SCHEMA IF NOT EXISTS public;")
    except:
        print("Error in DB teardown: ", sys.exc_info()[1])


@pytest.fixture(scope='session')
def test_client():
    """A fixture to yield the test client"""
    global DB
    app = create_app(__name__, 'testing')
    app.config['JWT_SECRET_KEY'] = app.config['SECRET']
    api = API(app, jwt)
    api = URLS(api, urls=urls_v1).get_api()
    DB = Database(connection).init_db()
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

    base = BaseTestClass()
    try:
        base.create_base_test_admin()
        base.create_base_test_user()
    except:
        pass

    client = api.app.test_client()
    ctx = api.app.app_context()
    ctx.push()
    yield client
    ctx.pop()
    tear_down_db()


@pytest.fixture(scope='module')
def create_admin_token():
    "a reusable function to create an admin token"
    try:
        user = User().login_user(BaseTestClass.base_admin['email'], BaseTestClass.base_admin['password'])
    except:
        BaseTestClass().create_base_test_admin()
        user = User().login_user(BaseTestClass.base_admin['email'], BaseTestClass.base_admin['password'])
    # create access token
    access_token_admin = create_access_token(identity=user)
    # create header
    header_admin = {
        'Authorization': 'Bearer {}'.format(access_token_admin)
    }
    return header_admin


@pytest.fixture(scope='module')
def create_user_token():
    """A reusable function to create a user token"""
    try:
        user = User().login_user(BaseTestClass.base_user['email'], BaseTestClass.base_user['password'])
    except:
        BaseTestClass.create_base_test_user()
        user = User().login_user(BaseTestClass.base_user['email'], BaseTestClass.base_user['password'])
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
