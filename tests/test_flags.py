import base64
import json
import time
from pytest import raises

from hackthebox import HTBClient, Machine, Challenge, Endgame, Fortress
from hackthebox.errors import (
    IncorrectFlagException,
    IncorrectArgumentException,
    RootAlreadySubmitted,
    UserAlreadySubmitted,
)

CORRECT_CHALLENGE = "HTB{a_challenge_flag}"
CORRECT_HASH = "30ea86803e0d85be51599c3a4e422266"
CORRECT_USER_HASH = "30ea86803e0d85be51599c3a4e422266"
CORRECT_ROOT_HASH = "179c07f9513e8f5474974fb7c96f3081"


def test_machine_flags(mock_htb_client: HTBClient):
    """Tests the ability to submit machine flags"""
    # Create a fake machine to test with
    machine = Machine(
        {
            "id": 1,
            "name": "Lame",
            "os": "Linux",
            "points": 0,
            "release": "2021-02-27T17:00:00.000000Z",
            "user_owns_count": 0,
            "root_owns_count": 0,
            "authUserInUserOwns": False,
            "authUserInRootOwns": False,
            "authUserHasReviewed": False,
            "stars": 0.0,
            "avatar": "nothing.png",
            "difficultyText": "Easy",
            "free": False,
            "maker": {"id": 1},
            "maker2": None,
        },
        mock_htb_client,
        summary=True,
    )
    assert machine.submit(CORRECT_USER_HASH, 10) == f"{machine.name} user is now owned."
    assert machine.submit(CORRECT_ROOT_HASH, 20) == f"{machine.name} root is now owned."

    with raises(IncorrectFlagException):
        machine.submit("wrong", 10)

    with raises(IncorrectArgumentException):
        machine.submit(CORRECT_HASH, 5)

    # change access token to have mock send already solved
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
                    "solved_this_machine": "1",
                    "scopes": [],
                }
            ).encode()
        ).decode()
        + "."
    )
    with raises(UserAlreadySubmitted):
        machine.submit(CORRECT_USER_HASH, 10)

    with raises(RootAlreadySubmitted):
        machine.submit(CORRECT_ROOT_HASH, 10)
    mock_htb_client._access_token = backup


def test_challenge_flags(mock_htb_client: HTBClient):
    """Tests the ability to submit challenge flags"""
    # Create a fake challenge to test with
    challenge = Challenge(
        {
            "id": 1,
            "name": "Crack This",
            "retired": True,
            "points": 0,
            "difficulty": "Easy",
            "difficulty_chart": "0",
            "release_date": "2018-04-25",
            "solves": 0,
            "authUserSolve": False,
            "likes": False,
            "dislikes": False,
        },
        mock_htb_client,
        summary=True,
    )
    assert challenge.submit(CORRECT_CHALLENGE, 10) is True

    with raises(IncorrectFlagException):
        challenge.submit("wrong", 10)

    with raises(IncorrectArgumentException):
        challenge.submit(CORRECT_CHALLENGE, 5)

    try:
        challenge.submit(CORRECT_CHALLENGE, 5)
    except IncorrectArgumentException as e:
        str(e)


def test_endgame_flags(mock_htb_client: HTBClient):
    """Tests the ability to submit endgame flags"""
    # Create a fake endgame to test with
    endgame = Endgame(
        {
            "id": 1,
            "name": "P.O.O.",
            "avatar_url": "nothing.png",
            "cover_image_url": "nothing.png",
            "retired": True,
            "vip": True,
            "creators": [
                {
                    "id": 302,
                    "name": "eks",
                },
                {
                    "id": 2984,
                    "name": "mrb3n",
                },
            ],
        },
        mock_htb_client,
        summary=True,
    )
    assert endgame.submit(CORRECT_HASH) is True

    with raises(IncorrectFlagException):
        endgame.submit("wrong")


def test_fortress_flags(mock_htb_client: HTBClient):
    """Tests the ability to submit fortress flags"""
    # Create a fake fortress to test with
    fortress = Fortress(
        {
            "id": 1,
            "name": "Jet",
            "ip": "10.13.37.10",
            "image": "https://www.hackthebox.eu/storage/companies/3.png",
            "number_of_flags": 11,
        },
        mock_htb_client,
        summary=True,
    )
    assert fortress.submit(CORRECT_HASH) is True

    with raises(IncorrectFlagException):
        fortress.submit("wrong")
