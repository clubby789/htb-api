from pytest import raises
from hackthebox import HTBClient, HTBObject
from hackthebox.solve import *


def test_get_user(htb_client: HTBClient):
    """Tests the ability to retrieve a specific user"""
    user = htb_client.get_user(83743)
    assert user.id == 83743
    assert user.name == "clubby789"
    print(user)


def test_get_non_existent_user(htb_client: HTBClient):
    """Tests for a failure upon a non existent user"""
    with raises(Exception):
        htb_client.get_user(10000000)


def test_get_user_team(htb_client: HTBClient):
    """Tests retrieving a Team from a User"""
    htb_bot = htb_client.get_user(16)
    assert htb_bot.team is not None

    # Joke account, should never have a team
    istarcheaters = htb_client.get_user(272569)
    assert istarcheaters.team is None


def test_get_activity(htb_client: HTBClient):
    """Tests retrieving a user's activity"""
    activity = htb_client.user.activity
    assert activity is not None
    print(repr(activity[0]))


def test_get_activity_items(htb_client: HTBClient):
    """Tests retrieving associated items from activity"""
    activity = htb_client.user.activity
    assert isinstance(activity[0].item, HTBObject)
    for solve_type in MachineSolve, ChallengeSolve:
        # TODO: Test Endgame and Fortress solves, when those are implemented
        solve_of_type = next(filter(lambda x: isinstance(x, solve_type), activity))
        assert solve_of_type.item is not None

