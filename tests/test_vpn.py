from pytest import raises
import base64
import json
import time

from hackthebox import HTBClient, Machine, Challenge, Endgame, Fortress
from hackthebox.errors import VpnException, CannotSwitchWithActive


def test_vpn_switch(mock_htb_client: HTBClient):
    """Tests the ability to switch vpn servers"""
    
    cur_vpn = mock_htb_client.get_current_vpn_server()
    all_vpns = mock_htb_client.get_all_vpn_servers()
    new_vpn = all_vpns[5]
    resp = new_vpn.switch()
    assert resp


    # change access token to have mock send no active machine
    backup = mock_htb_client._access_token
    # mock_htb_client._access_token = "eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJSUzI1NiJ9.eyJhdWQiOiAiMCIsICJqdGkiOiAiIiwgImlhdCI6IDAsICJuYmYiOiAwLCAiZXhwIjogMTk0NTg3NTEyNC45MjY5NTEyLCAic3ViIjogIjAiLCAic2NvcGVzIjogWyBdfSIK."
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
                    "has_active_machine": "1",
                    "scopes": [],
                }
            ).encode()
        ).decode()
        + "."
    )

    with raises(CannotSwitchWithActive):
        new_vpn.switch()
    mock_htb_client._access_token = backup


def test_vpn_get_current(mock_htb_client: HTBClient):
    """Test getting the current vpn server"""
    cur_vpn = mock_htb_client.get_current_vpn_server()
    assert cur_vpn.friendly_name == 'EU VIP 20'

    cur_ra_vpn = mock_htb_client.get_current_vpn_server(release_arena=True)
    assert cur_ra_vpn.friendly_name == "EU Release Lab 1"
   
