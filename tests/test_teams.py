from pytest import raises
from hackthebox import HTBClient


def test_get_team(mock_htb_client: HTBClient):
    """Tests the ability to retrieve a specific team"""
    team = mock_htb_client.get_team(2710)
    assert team.id == 2710
    assert team.name == "TheWINRaRs"
    print(team)


def test_get_non_existent_team(mock_htb_client: HTBClient):
    """Tests for a failure upon a non existent team"""
    with raises(Exception):
        mock_htb_client.get_team(10000000)


def test_get_ranking(mock_htb_client: HTBClient):
    team = mock_htb_client.get_team(2710)
    assert team.ranking is not None


def test_get_captain(mock_htb_client: HTBClient):
    admins = mock_htb_client.get_team(21)
    assert admins.captain.name == "ch4p"
