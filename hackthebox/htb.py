from __future__ import annotations
from typing import List, Callable
import base64
import json
import time

import requests

from .constants import API_BASE, USER_AGENT
from .errors import AuthenticationException, MissingPasswordException, MissingEmailException


def jwt_expired(token: str) -> bool:
    """ Checks if a JWT token is expired

    Args:
        token: A JWT string - 3 Base64 sequences joined with .

    Returns:
        If the token is expired

    """
    payload = base64.b64decode(token.split('.')[1]).decode()
    if time.time() > json.loads(payload)['exp']:
        return True
    else:
        return False


class HTBClient:
    """The client via which API requests are made

    Examples:
        Connecting to the API::

            from hackthebox import HTBClient
            client = HTBClient(email="user@example.com", password="S3cr3tP455w0rd!")

    """
    # noinspection PyUnresolvedReferences
    _user: "User" = None
    _access_token: str = None
    _refresh_token: str = None
    _api_base: str = None

    def _refresh_access_token(self):
        """

        Use a saved refresh token to gain a new access token
        when the current one expires

        """
        headers = {"User-Agent": USER_AGENT}
        r = requests.post(API_BASE + "login/refresh", json={
                "refresh_token": self._refresh_token
            }, headers=headers)
        data = r.json()['message']
        self._access_token = data['access_token']
        self._refresh_token = data['refresh_token']

    def do_request(self, endpoint, json_data=None, data=None, authorized=True) -> dict:
        """

        Args:
            endpoint: The API endpoint to request
            json_data: Data to be sent in JSON format
            data: Data to be sent in application/x-www-form-urlencoded format
            authorized: If the request requires an Authorization header
        Returns:
            The JSON response from the API

        """
        headers = {"User-Agent": USER_AGENT}
        if authorized and self._api_base == API_BASE:
            # Don't use authorization if the API base URL isn't the real one -
            # i.e. we're running a test
            if jwt_expired(self._access_token):
                self._refresh_access_token()
            headers['Authorization'] = "Bearer " + self._access_token
        while True:
            if not json_data and not data:
                r = requests.get(self._api_base + endpoint, headers=headers)
            else:
                r = requests.post(self._api_base + endpoint, json=json_data, data=data, headers=headers)
            if r.status_code != 429:
                break
            # Not sure on the exact ratelimit - loop until we don't get 429
            else:
                time.sleep(0.25)
        return r.json()

    def __init__(self, email: str = None, password: str = None, api_base: str = API_BASE):
        self._api_base = api_base
        if not password and not email:
            print("Must give an authentication method")
            raise AuthenticationException
        elif password and not email:
            raise MissingEmailException
        elif email and not password:
            raise MissingPasswordException
        else:
            data = self.do_request("login", json_data={
                "email": email, "password": password
            }, authorized=False)
            self._access_token = data['message']['access_token']
            self._refresh_token = data['message']['refresh_token']

    # noinspection PyUnresolvedReferences
    def do_search(self, search_term: str) -> "Search":
        from .search import Search
        return Search(search_term, self)

    # noinspection PyUnresolvedReferences
    def get_machine(self, machine_id: int) -> "Machine":
        """

        Args:
            machine_id: The platform ID of the `Machine` to fetch

        Returns: The requested `Machine`

        """
        from .machine import Machine
        data = self.do_request(f"machine/profile/{machine_id}")['info']
        return Machine(data, self)

    # noinspection PyUnresolvedReferences
    def get_machines(self, limit: int = None, retired: bool = False) -> List["Machine"]:
        """

        Retrieve a list of `Machine` from the API

        Args:
            limit: The maximum number to fetch
            retired: Whether to fetch from the retired list instead of the active list

        Returns: A list of `Machine`

        """
        from .machine import Machine
        if not retired:
            data = self.do_request("machine/list")['info'][:limit]
        else:
            data = self.do_request("machine/list/retired")['info'][:limit]
        return [Machine(m, self, summary=True) for m in data]

    # noinspection PyUnresolvedReferences
    def get_challenge(self, challenge_id: int) -> "Challenge":
        """

        Args:
            challenge_id: The platform ID of the `Challenge` to fetch

        Returns: The requested `Challenge`

        """
        from .challenge import Challenge
        data = self.do_request(f"challenge/info/{challenge_id}")['challenge']
        return Challenge(data, self)

    # noinspection PyUnresolvedReferences
    def get_challenges(self, limit=None, retired=False) -> List["Challenge"]:
        """Requests a list of `Challenge` from the API

        Args:
            limit: The maximum number of `Challenge` to fetch
            retired: Whether to fetch from the retired list instead of the active list

        Returns: A list of `Challenge`

        """
        from .challenge import Challenge
        if retired:
            data = self.do_request("challenge/list/retired")
        else:
            data = self.do_request("challenge/list")
        challenges = []
        for challenge in data['challenges'][:limit]:
            challenges.append(Challenge(challenge, self, summary=True))
        return challenges

    # noinspection PyUnresolvedReferences
    def get_endgame(self, endgame_id: int) -> "Endgame":
        """Requests an Endgame from the API

        Args:
            endgame_id: The ID of the Endgame to fetch

        Returns: An Endgame

        """
        from .endgame import Endgame
        data = self.do_request(f"endgame/{endgame_id}")["data"]
        return Endgame(data, self)

    # noinspection PyUnresolvedReferences
    def get_endgames(self, limit: int = None) -> List["Endgame"]:
        """Requests a list of Endgames from the API

        Args:
            limit: The maximum number of Endgames to fetch

        Returns: A list of Endgames

        """
        from .endgame import Endgame
        data = self.do_request(f"endgames")["data"][:limit]
        endgames = []
        for endgame in data:
            endgames.append(Endgame(endgame, self, summary=True))
        return endgames

    # noinspection PyUnresolvedReferences
    def get_fortress(self, fortress_id: int) -> "Fortress":
        """Requests an Fortress from the API

        Args:
            fortress_id: The ID of the Fortress to fetch

        Returns: A Fortresse

        """
        from .fortress import Fortress
        data = self.do_request(f"fortress/{fortress_id}")["data"]
        return Fortress(data, self)

    # noinspection PyUnresolvedReferences
    def get_fortresses(self, limit: int = None) -> List["Fortress"]:
        """Requests a list of Fortresses from the API

        Args:
            limit: The maximum number of Fortresses to fetch

        Returns: A list of Fortresses

        """
        from .fortress import Fortress
        data = self.do_request(f"fortresses")["data"]
        fortresses = []
        # For some  reason, the fortress list is in the format {"1": <fortress1>, "2": <fortress2>}
        # instead of [<fortress1>, <fortress2>], meaning we have to sort it ourselves
        for fortress_id, fortress in sorted(data.items())[:limit]:
            fortresses.append(Fortress(fortress, self, summary=True))
        return fortresses

    # noinspection PyUnresolvedReferences
    def get_user(self, user_id: int) -> "User":
        """

        Args:
            user_id: The platform ID of the `User` to fetch

        Returns: The requested `User`

        """
        from .user import User
        data = self.do_request(f"user/profile/basic/{user_id}")['profile']
        return User(data, self)

    # noinspection PyUnresolvedReferences
    def get_team(self, team_id: int) -> "Team":
        """

        Args:
            team_id: The platform ID of the `Team` to fetch

        Returns: The requested `Team`

        """
        from .team import Team
        data = self.do_request(f"team/info/{team_id}")
        return Team(data, self)

    # noinspection PyUnresolvedReferences
    def get_hof(self, vip: bool = False) -> "Leaderboard":
        from .leaderboard import Leaderboard
        from .user import User
        """
        Returns: A Leaderboard of Users
        """
        endpoint = "rankings/users"
        if vip:
            endpoint += "?vip=1"
        data = self.do_request(endpoint)['data']
        return Leaderboard(data, self, User)

    # noinspection PyUnresolvedReferences
    def get_hof_countries(self) -> "Leaderboard":
        from .leaderboard import Leaderboard, Country
        """
        Returns: A Leaderboard of Countries
        """
        data = self.do_request("rankings/countries")['data']
        return Leaderboard(data, self, Country)

    # noinspection PyUnresolvedReferences
    def get_hof_teams(self) -> "Leaderboard":
        """

        Returns: A Leaderboard of Teams

        """
        from .leaderboard import Leaderboard
        from .team import Team
        data = self.do_request("rankings/teams")['data']
        return Leaderboard(data, self, Team)

    # noinspection PyUnresolvedReferences
    def get_hof_universities(self) -> "Leaderboard":
        """
        Returns: A Leaderboard of Universities

        """
        from .leaderboard import Leaderboard, University
        data = self.do_request("rankings/universities")['data']
        return Leaderboard(data, self, University)

    # noinspection PyUnresolvedReferences
    @property
    def user(self) -> "User":
        """

        Returns: The `User` associated with the current `HTBClient`

        """
        if not self._user:
            uid = self.do_request("user/info")['info']['id']
            self._user = self.get_user(uid)
        return self._user


class HTBObject:
    """ Base class of all API objects

    Attributes:
        id: The ID of the associated object
    """
    _client: HTBClient
    # Attributes not fetched by a summary
    _detailed_attributes: List[str]
    _detailed_func: Callable
    _is_summary: bool = False
    id: int

    def __getattr__(self, item):
        """Retrieve attributes not given when initialised from a summary

        Some endpoints only provide a subset of the attributes available for a given object.
        If these extra attributes are requested, the object will request the full data from the
        API and fill out the missing items.

        Args:
            item: The name of the property to retrieve

        """
        if item in self._detailed_attributes and self._is_summary:
            new_obj = self._detailed_func(self.id)
            for attr in self._detailed_attributes:
                setattr(self, attr, getattr(new_obj, attr))
            self._is_summary = False
            return getattr(new_obj, item)
        else:
            raise AttributeError
