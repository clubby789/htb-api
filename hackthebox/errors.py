class HtbException(Exception):
    """Base exception class for `hackthebox`"""
    pass


class AuthenticationException(HtbException):
    """An error authenticating to the API"""
    pass


class MissingEmailException(AuthenticationException):
    """An email was not given where it was required"""
    pass


class MissingPasswordException(AuthenticationException):
    """A password was not given where it was required"""
    pass


class UnknownSolveException(HtbException):
    """An unknown solve type was passed"""
    pass


class IncorrectFlagException(HtbException):
    """An incorrect flag was submitted"""
    pass


class IncorrectArgumentException(HtbException):
    """An incorrectly formatted argument was passed"""

    reason: str

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"IncorrectArgumentException(reason='{self.reason}')"

    def __init__(self, reason: str):
        self.reason = reason
    pass
