from pytest import raises
from hackthebox.htb import HTBClient
from hackthebox import errors


def test_login(htb_client: HTBClient):
    """Tests the ability to login and receive a bearer token"""
    assert htb_client._access_token is not None


def test_incorrect_login():
    with raises(errors.AuthenticationException):
        HTBClient()
    with raises(errors.AuthenticationException):
        HTBClient(password="wrong")
    with raises(errors.AuthenticationException):
        HTBClient(email="wrong@wrong.com")


def test_get_own_user(htb_client: HTBClient):
    assert htb_client.user is not None


def test_invalid_attr(htb_client: HTBClient):
    """Tests that getting an invalid attr from a HTBObject
    doesn't cause infinite recursion or similar problems"""
    with raises(AttributeError):
        print(htb_client.get_machine(1).nothing)


def test_refresh_token(expired_htb_client: HTBClient):
    """Tests the ability to refresh an expired access token"""
    expired_htb_client.get_machine(1)
