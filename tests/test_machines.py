from pytest import raises
import base64
import json
import time

from hackthebox import HTBClient


def test_get_machine(mock_htb_client: HTBClient):
    """Tests the ability to retrieve a specific machine"""
    machine = mock_htb_client.get_machine(1)
    assert machine.id == 1
    assert machine.name == "Lame"
    repr(machine)


def test_get_active_machine(mock_htb_client: HTBClient):
    """Tests the ability to retrieve active machine"""

    # by default there is an active machine
    machine = mock_htb_client.get_active_machine()
    assert machine.id == 387
    assert machine.name == "Driver"

    # change access token to have mock send no active machine
    backup = mock_htb_client._access_token
#    mock_htb_client._access_token = "eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJSUzI1NiJ9.eyJhdWQiOiAiMCIsICJqdGkiOiAiIiwgImlhdCI6IDAsICJuYmYiOiAwLCAiZXhwIjogMTk0NTg3NTEyNC45MjY5NTEyLCAic3ViIjogIjAiLCAic2NvcGVzIjogWyBdfSIK."
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
                    "exp": time.time() + 100,
                    "sub": "0",
                    "no_active": "1",
                    "scopes": [],
                }
            ).encode()
        ).decode()
        + "."
    )
 
    machine = mock_htb_client.get_active_machine()
    assert machine is None
    mock_htb_client._access_token = backup


def test_get_solves(mock_htb_client: HTBClient):
    """Tests the ability to retrieve a specific machine"""
    machine = mock_htb_client.get_machine(1)
    repr(machine.root_blood)
    assert machine.root_blood.machine == machine


def test_get_non_existent_machine(mock_htb_client: HTBClient):
    """Tests for a failure upon a non existent challenge"""
    with raises(Exception):
        mock_htb_client.get_machine(10000000)


def test_list_machines(mock_htb_client: HTBClient):
    """Tests that the challenges can be listed"""
    machines = mock_htb_client.get_machines()
    assert len(machines) >= 20
    retired = mock_htb_client.get_machines(retired=True)
    assert len(retired) >= 150


def test_machine_author(mock_htb_client: HTBClient):
    """Tests retrieving the author of a machine"""
    machine = mock_htb_client.get_machine(1)
    author = machine.authors[0]
    assert author.name == "ch4p"
