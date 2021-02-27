from pytest import raises
from hackthebox import HTBClient, Machine, Challenge
from hackthebox.errors import IncorrectFlagException, IncorrectArgumentException


CORRECT_CHALLENGE = "HTB{a_challenge_flag}"
CORRECT_HASH = "30ea86803e0d85be51599c3a4e422266"


def test_machine_flags(mock_htb_client: HTBClient):
    """Tests the ability to submit machine flags"""
    # Create a fake machine to test with
    machine = Machine({
        "id": 1,
        "name": "Lame",
        "os": "Linux",
        "points": 0,
        "release": "N/A",
        "user_owns_count": 0,
        "root_owns_count": 0,
        "authUserInUserOwns": False,
        "authUserInRootOwns": False,
        "authUserHasReviewed": False,
        "stars": 0.0,
        "avatar": "nothing.png",
        "difficultyText": "Easy",
        "free": False,
        "maker": {
            "id": 1
        },
        "maker2": None
    }, mock_htb_client, summary=True)
    assert machine.submit(CORRECT_HASH, 10) is True

    with raises(IncorrectFlagException):
        machine.submit("wrong", 10)

    with raises(IncorrectArgumentException):
        machine.submit(CORRECT_HASH, 5)


def test_challenge_flags(mock_htb_client: HTBClient):
    """Tests the ability to submit challenge flags"""
    # Create a fake machine to test with
    challenge = Challenge({
        "id": 1,
        "name": "Crack This",
        "retired": True,
        "points": 0,
        "difficulty_chart": "0",
        "solves": 0,
        "authUserSolve": False,
        "likes": False,
        "dislikes": False
    }, mock_htb_client, summary=True)
    assert challenge.submit(CORRECT_CHALLENGE, 10) is True

    with raises(IncorrectFlagException):
        challenge.submit("wrong", 10)

    with raises(IncorrectArgumentException):
        challenge.submit(CORRECT_CHALLENGE, 5)
