"""This file contains all custom exceptions that will be thrown in the application"""


class AlreadyExists(Exception):
    """handle item already exist already"""

    def __init__(self):
        """
        Initialise the exception
        """
        Exception.__init__(self, "The item you tried to add already exists")
