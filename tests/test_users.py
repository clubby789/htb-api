from pytest import raises

from hackthebox import HTBClient
from hackthebox.solve import *


def test_get_user(mock_htb_client: HTBClient):
    """Tests the ability to retrieve a specific user"""
    user = mock_htb_client.get_user(83743)
    assert user.id == 83743
    assert user.name == "clubby789"
    repr(user)


def test_get_non_existent_user(mock_htb_client: HTBClient):
    """Tests for a failure upon a non existent user"""
    with raises(Exception):
        mock_htb_client.get_user(10000000)


def test_get_user_team(mock_htb_client: HTBClient):
    """Tests retrieving a Team from a User"""
    htb_bot = mock_htb_client.get_user(16)
    assert htb_bot.team is not None

    # Joke account, should never have a team
    istarcheaters = mock_htb_client.get_user(272569)
    assert istarcheaters.team is None


def test_get_activity(mock_htb_client: HTBClient):
    """Tests retrieving a user's activity"""
    activity = mock_htb_client.user.activity
    assert activity is not None
    if len(activity) > 0:
        repr(activity[0])


def test_get_activity_items(mock_htb_client: HTBClient):
    """Tests retrieving associated items from activity"""
    activity = mock_htb_client.user.activity
    if len(activity) > 0:
        assert isinstance(activity[0].item, HTBObject)
        for solve_type in MachineSolve, ChallengeSolve, EndgameSolve, FortressSolve:
            solve_of_type = next(filter(lambda x: isinstance(x, solve_type), activity))
            assert solve_of_type.item is not None


def test_get_content(mock_htb_client: HTBClient):
    """Test getting content generated by the user"""
    user = mock_htb_client.get_user(83743)
    content = user.get_content()
    assert len(content.machines) == 1
    machines = user.get_machines()
    assert machines[0].name == "Obscurity"
    challenges = user.get_challenges()
    assert len(challenges) == 3
    assert "Crack This!" in [c.name for c in challenges]
