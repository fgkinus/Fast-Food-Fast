"""This file contains all custom exceptions that will be thrown in the application"""


class SystemException(Exception):
    """Base exception for all custom Exceptions"""
    pass


class AlreadyExists(SystemException):
    """handle item already exist already"""
    pass


class AttributeNotFound(SystemException):
    """An exception thrown when setting an undefined exception"""
    pass


class StoredProcedureError(SystemException):
    """an exception raised when a stored procedure exception occur"""
    pass
