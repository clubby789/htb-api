import pytest
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
