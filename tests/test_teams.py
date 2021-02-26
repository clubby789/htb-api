import pytest
from pytest import raises
from hackthebox import HTBClient


def test_get_team(htb_client: HTBClient):
    """Tests the ability to retrieve a specific team"""
    team = htb_client.get_team(2710)
    assert team.id == 2710
    assert team.name == "TheWINRaRs"
    print(team)


def test_get_non_existent_team(htb_client: HTBClient):
    """Tests for a failure upon a non existent team"""
    with raises(Exception):
        htb_client.get_team(10000000)


def test_get_ranking(htb_client: HTBClient):
    team = htb_client.get_team(2710)
    assert team.ranking is not None


def test_get_captain(htb_client: HTBClient):
    admins = htb_client.get_team(21)
    assert admins.captain.name == "ch4p"
