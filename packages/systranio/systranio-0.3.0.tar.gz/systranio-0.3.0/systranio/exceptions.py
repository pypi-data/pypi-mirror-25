"""
Exceptions
"""

class ParameterError(AttributeError):
    """
    Invalid API Parameter set
    """


class ApiKeyError(ValueError):
    """
    Systran.io refused the key provided
    """

class ApiFailure(Exception):
    """
    Systran.io returned a 500 error
    """
