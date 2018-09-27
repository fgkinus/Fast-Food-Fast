"""CLasses with methods to interact with the Database """

from app.V1.Accounts.Models import User as Base, UserSchema
from app.V2 import DB


class User(Base):
    """User Model to interact with the DB"""

    def __init__(self):
        """initialise the class"""
        self.parser = UserSchema()

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
