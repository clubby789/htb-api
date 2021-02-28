from pytest import raises
from hackthebox import HTBClient


def test_get_challenge(htb_client: HTBClient):
    """Tests the ability to retrieve a specific challenge"""
    challenge = htb_client.get_challenge(69)
    assert challenge.id == 69
    assert challenge.name == "TheFutureBender"
    assert challenge.retired
    print(challenge)


def test_get_non_existent_challenge(htb_client: HTBClient):
    """Tests for a failure upon a non existent challenge"""
    with raises(Exception):
        htb_client.get_challenge(10000000)


def test_get_challenges(htb_client: HTBClient):
    """Tests that the challenges can be listed"""
    challenges = htb_client.get_challenges(limit=30)
    assert len(challenges) == 30
    challenges = htb_client.get_challenges(limit=30, retired=True)
    assert len(challenges) == 30


def test_fill_in_summary(htb_client: HTBClient):
    """Test that partial `Challenges` can be 'filled in'"""
    challenge = htb_client.get_challenges(limit=1)[0]
    assert challenge.description is not None


def test_challenge_author(htb_client: HTBClient):
    """Tests retrieving the author of a machine"""
    challenge = htb_client.get_challenge(1)
    author = challenge.authors[0]
    assert author.name == "Thiseas"
