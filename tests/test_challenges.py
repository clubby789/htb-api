import os

from pytest import raises
from hackthebox import HTBClient, NoDockerException, NoDownloadException, RateLimitException


def test_get_challenge(mock_htb_client: HTBClient):
    """Tests the ability to retrieve a specific challenge"""
    challenge = mock_htb_client.get_challenge(1)
    assert challenge.id == 1
    assert challenge.name == "Crack This!"
    assert challenge.retired
    print(challenge)


def test_get_non_existent_challenge(mock_htb_client: HTBClient):
    """Tests for a failure upon a non existent challenge"""
    with raises(Exception):
        mock_htb_client.get_challenge(10000000)


def test_get_challenges(mock_htb_client: HTBClient):
    """Tests that the challenges can be listed"""
    challenges = mock_htb_client.get_challenges(limit=30)
    assert len(challenges) == 30
    challenges = mock_htb_client.get_challenges(limit=30, retired=True)
    assert len(challenges) == 30


def test_fill_in_summary(mock_htb_client: HTBClient):
    """Test that partial `Challenges` can be 'filled in'"""
    challenge = mock_htb_client.get_challenges(limit=1)[0]
    assert challenge.description is not None


def test_challenge_authors(mock_htb_client: HTBClient):
    """Tests retrieving the authors of a machine"""
    challenge = mock_htb_client.get_challenge(196)
    author1, author2 = challenge.authors
    assert author1.name == "makelarisjr"
    assert author2.name == "makelaris"


def test_start_challenge(mock_htb_client: HTBClient):
    """Tests the ability to start an instance of a challenge"""
    # Use mock API for the starting so we don't spam
    bad_challenge = mock_htb_client.get_challenge(1)
    with raises(NoDockerException):
        bad_challenge.start()

    # TODO: Test loading a started challenge on the API
    # Will require the mock API tracking the challenges which have 'started'
    good_challenge = mock_htb_client.get_challenge(143)
    instance = good_challenge.start()
    assert instance.ip is not None
    instance.stop()


def test_download_challenge(mock_htb_client: HTBClient):
    """Tests the ability to download a challenge"""
    downloadable = mock_htb_client.get_challenge(1)
    not_downloadable = mock_htb_client.get_challenge(119)

    path = downloadable.download()
    assert os.path.exists(path)
    os.remove(path)
    downloadable._client.challenge_cooldown = 253407876721
    # The year 10,000 - should be fine
    with raises(RateLimitException):
        downloadable.download()
    downloadable._client.challenge_cooldown = 0
    with raises(NoDownloadException):
        not_downloadable.download()
