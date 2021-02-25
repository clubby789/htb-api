from hackthebox.htb import HTBClient


def test_login(htb_client: HTBClient):
    """Tests the ability to login and receive a bearer token"""
    assert htb_client._access_token is not None

