from pytest import raises
from hackthebox.htb import HTBClient


def test_login(htb_client: HTBClient):
    """Tests the ability to login and receive a bearer token"""
    assert htb_client._access_token is not None


def test_incorrect_login():
    # TODO: Add API-specific exceptions
    with raises(Exception):
        HTBClient()
    with raises(Exception):
        HTBClient(password="wrong")
    with raises(Exception):
        HTBClient(email="wrong@wrong.com")


def test_get_own_user(htb_client: HTBClient):
    assert htb_client.user is not None
