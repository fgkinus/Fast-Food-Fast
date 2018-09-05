from app.Accounts import Models
from passlib.hash import pbkdf2_sha256 as sha256


class TestAccounts(object):
    """test cases for User Object"""

    def test_user_create(self):
        user = Models.User().add_user(username='test', firstname='firstname', surname='sir', secondname='second',
                                      password='pass',
                                      email='test@test.com')
        assert user.username == 'test'
        assert hasattr(user, 'password') is True

    def test_admin_create(self):
        user = Models.Admin().add_user(username='test-admin', firstname='firstname', surname='sir', secondname='second',
                                       password='pass',
                                       email='test@admin.com')
        assert user.username == 'test-admin'
        assert hasattr(user, 'password') is True
        assert hasattr(user, 'email') is True

    def test_password_encryption(self):
        user = Models.User().add_user(username='test', firstname='firstname', surname='sir', secondname='second',
                                      password='pass',
                                      email='test@test.com')
        assert user.password != 'pass'

    def test_password_decryption(self):
        user = Models.Admin().add_user(username='test-admin', firstname='firstname', surname='sir', secondname='second',
                                       password='pass',
                                       email='test@admin.com')

        assert sha256.verify('pass', user.password)

    def test_user_is_not_admin(self):
        user = Models.User().add_user(username='test', firstname='firstname', surname='sir', secondname='second',
                                      password='pass',
                                      email='test@test.com')

        assert user.get_admin_status() is False

    def test_admin_is_admin(self):
        user = Models.Admin().add_user(username='test-admin', firstname='firstname', surname='sir', secondname='second',
                                       password='pass',
                                       email='test@admin.com')
        assert user.get_admin_status() is True

    def test_set_user_id_method(self):
        number = len(Models.users)
        user = Models.User().add_user(username='test-admin', firstname='firstname', surname='sir', secondname='second',
                                      password='pass',
                                      email='test@admin.com')
        assert user.ID == number + 1
        assert len(Models.users) == user.ID

    def test_set_admin_id_method(self):
        number = len(Models.admin)
        user = Models.Admin().add_user(username='test-admin', firstname='firstname', surname='sir', secondname='second',
                                       password='pass',
                                       email='test@admin.com')
        assert user.ID == number + 1
        assert len(Models.admin) == user.ID

    def test_update_user_details(self):
        user = Models.User().add_user(username='test-admin', firstname='firstname', surname='sir', secondname='second',
                                      password='pass',
                                      email='test@admin.com')
        user.surname = 'surname'
        user.update_user_list()

        for u in Models.users:
            if u.ID == user.ID:
                assert u.surname == 'surname'

    def test_email_validation(self):
        email = 'test@emai.com'
        assert Models.User().validate_email(email) is True

    def test_email_validation_admin(self):
        email = 'testemai.com'
        assert Models.Admin().validate_email(email) is False
