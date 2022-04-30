import base64
import json

from pytest import raises

from hackthebox import errors
from hackthebox.htb import HTBClient


def test_login(mock_htb_client: HTBClient):
    """Tests the ability to login and receive a bearer token"""
    assert mock_htb_client._access_token is not None


def test_app_token_login(token_mock_htb_client: HTBClient):
    """Tests the ability to login and receive a bearer token"""
    assert token_mock_htb_client._app_token is not None
    assert (
        token_mock_htb_client._access_token
        == token_mock_htb_client._refresh_token
        is None
    )


def test_interactive_login(monkeypatch):
    from io import StringIO
    import random

    from mock_api.app import start_server
    import time

    port = random.randint(1024, 65535)
    start_server(port)
    # Wait for server thread to start
    time.sleep(0.5)
    inp1 = StringIO("user@example.com\n")
    inp2 = "password"
    monkeypatch.setattr("sys.stdin", inp1)
    monkeypatch.setattr("getpass.getpass", lambda: inp2)

    client = HTBClient(api_base=f"http://localhost:{port}/api/v4/")
    assert client._access_token is not None


def test_otp_login():
    """Tests the OTP functionality"""
    import random
    from mock_api.app import start_server
    import time

    port = random.randint(1024, 65535)
    thread = start_server(port)
    # Wait for server thread to start
    time.sleep(0.5)

    with raises(errors.IncorrectOTPException):
        HTBClient(
            email="otpuser@example.com",
            password="password",
            otp=555555,
            api_base=f"http://localhost:{port}/api/v4/",
        )
    client = HTBClient(
        email="otpuser@example.com",
        password="password",
        otp=111111,
        api_base=f"http://localhost:{port}/api/v4/",
    )
    data = json.loads(base64.b64decode(client._access_token.split(".")[1] + "=="))
    exp = data["exp"]
    assert time.time() < exp <= time.time() + 100

    client = HTBClient(
        email="otpuser@example.com",
        password="password",
        otp=111111,
        api_base=f"http://localhost:{port}/api/v4/",
        remember=True,
    )
    data = json.loads(base64.b64decode(client._access_token.split(".")[1] + "=="))
    exp = data["exp"]
    assert time.time() + 29 * 24 * 60 * 60 < exp <= time.time() + 30 * 24 * 60 * 60


def test_get_own_user(mock_htb_client: HTBClient):
    assert mock_htb_client.user is not None


def test_invalid_attr(mock_htb_client: HTBClient):
    """Tests that getting an invalid attr from a HTBObject
    doesn't cause infinite recursion or similar problems"""
    with raises(AttributeError):
        repr(mock_htb_client.get_machine(1).nothing)


def test_refresh_token(mock_htb_client: HTBClient):
    import base64
    import json

    """Tests the ability to refresh an expired access token"""
    token = mock_htb_client._access_token
    mock_htb_client._access_token = (
        base64.b64encode(json.dumps({"typ": "JWT", "alg": "RS256"}).encode()).decode()
        + "."
        + base64.b64encode(
            json.dumps(
                {
                    "aud": "0",
                    "jti": "",
                    "iat": 0,
                    "nbf": 0,
                    "exp": 0,
                    "sub": "0",
                    "scopes": [],
                }
            ).encode()
        ).decode()
        + "."
    )
    assert mock_htb_client.get_machine(1) is not None
