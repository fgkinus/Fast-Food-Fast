"""This file contains all custom exceptions that will be thrown in the application"""


class SystemException(Exception):
    """Base exception for all custom Exceptions"""
    pass


class AlreadyExists(SystemException):
    """handle item already exist already"""
    pass
