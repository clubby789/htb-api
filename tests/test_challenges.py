import os

from pytest import raises
from hackthebox import HTBClient, NoDockerException, NoDownloadException


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


def test_challenge_authors(htb_client: HTBClient):
    """Tests retrieving the authors of a machine"""
    challenge = htb_client.get_challenge(196)
    author1, author2 = challenge.authors
    assert author1.name == "makelarisjr"
    assert author2.name == "makelaris"


def test_start_challenge(htb_client: HTBClient, mock_htb_client: HTBClient):
    """Tests the ability to start an instance of a challenge"""
    # Use mock API for the starting so we don't spam
    bad_challenge = htb_client.get_challenge(1)
    bad_challenge._client = mock_htb_client
    with raises(NoDockerException):
        bad_challenge.start()

    # TODO: Test loading a started challenge on the API
    # Will require the mock API tracking the challenges which have 'started'
    good_challenge = htb_client.get_challenge(144)
    good_challenge._client = mock_htb_client
    instance = good_challenge.start()
    assert instance.ip is not None
    instance.stop()


def test_download_challenge(htb_client: HTBClient):
    """Tests the ability to download a challenge"""
    path = htb_client.get_challenge(1).download()
    assert os.path.exists(path)
    os.remove(path)
    with raises(NoDownloadException):
        htb_client.get_challenge(143).download()
