"""CLasses with methods to interact with the Database """
from flask_restplus import Resource

from app.V1.Accounts.Models import User as Base, UserSchema


class User(Base):
    """User Model to interact with the DB"""

    def __init__(self):
        """initialise the class"""
        self.parser = UserSchema()

    def add_user(self,details):
        """
        Add a  user to the DB and return the user
        :param details:
        :return: user
        """
        user = self.parser.dump(details)
