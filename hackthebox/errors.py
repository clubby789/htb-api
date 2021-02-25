class HtbException(Exception):
    """Base exception class for `hackthebox`"""
    pass


class AuthenticationException(Exception):
    """An error authenticating to the API"""
    pass


class UnknownSolveException(Exception):
    """An unknown solve type was passed"""
    pass
