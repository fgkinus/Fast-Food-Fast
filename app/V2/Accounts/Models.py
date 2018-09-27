"""CLasses with methods to interact with the Database """
from flask_restplus import abort

from app.V1.Accounts.Models import User as Base, UserSchema
from app.V2 import DB


class User(Base):
    """User Model to interact with the DB"""

    def __init__(self):
        """initialise the class"""
        self.parser = UserSchema()
        self.user = None

    def add_user(self, details):
        """
        Add a  user to the DB and return the user
        :param details:
        :return: user
        """
        details = dict(details)
        details.update({'isadmin': False})
        details['password'] = self.generate_hash(details['password'])
        details = (
            details['username'],
            details['first_name'],
            details['second_name'],
            details['surname'],
            details['email'],
            details['password'],
            details['isadmin'],
        )
        DB.execute_procedures('add_user', details)

    def add_admin(self, details):
        """
        Add a  user to the DB and return the user
        :param details:
        :return: user
        """
        details = dict(details)
        details.update({'isadmin': True})
        details['password'] = self.generate_hash(details['password'])
        details = (
            details['username'],
            details['first_name'],
            details['second_name'],
            details['surname'],
            details['email'],
            details['password'],
            details['isadmin'],
        )
        DB.execute_procedures('add_user', details)

    def login_user(self, email, password):
        """a method to login users"""
        try:
            user = DB.execute_procedures('get_user_by_email', (email,))
        except Exception:
            DB.logger.info("user details for email {0} not found".format(email))
            abort(401, "user email not found")

        # validate password
        val = self.verify_hash(password, user[0]['password'])
        if val is False:
            abort(401, "wrong password")

        # return user instance
        self.user = user[0]
        return self

    def get_admin_status(self):
        """
        return the admin status of the user. Defaults to False
        :return: Bool
        """
        if self.user is not None:
            return self.user['isadmin']
        else:
            return False

    @staticmethod
    def get_user_by_username(username):
        """
        get user details by username
        :param username:
        :return: user
        """
        user = DB.execute_procedures('get_users_by_username', (username,))

        if len(user) == 0:
            DB.logger.debug("user details for {0} not found".format(username))
            abort(200, "user details for {0} not found".format(username))
        else:
            return user[0]

    @staticmethod
    def edit_user(original, updated):
        """
        Accept the original and updated user details and update the database
        :param original:
        :param updated:
        :return: updated
        """
        user_id = original['id']
        updated.update({'isadmin': original['isadmin']})
        details = (
            user_id,
            updated['username'],
            updated['first_name'],
            updated['second_name'],
            updated['surname'],
            updated['email'],
            updated['password'],
            updated['isadmin'],
        )
        new_details = DB.execute_procedures('modify_user', details)

        return new_details[0]
