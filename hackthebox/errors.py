class HtbException(Exception):
    """Base exception class for `hackthebox`"""
    pass


class AuthenticationException(HtbException):
    """An error authenticating to the API"""
    pass


class IncorrectFlagException(HtbException):
    """An incorrect flag was submitted"""
    pass


class IncorrectArgumentException(HtbException):
    """An incorrectly formatted argument was passed"""
    pass
