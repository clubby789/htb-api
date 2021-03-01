from typing import List

from .user import User
from .machine import Machine
from .team import Team
from .challenge import Challenge
from . import htb


class Search:
    """ Representation of a search on the platform

    Attributes:
        users: Users returned by the Search
        machines: Machines returned by the Search
        teams: Teams returned by the Search
        challenges: Challenges returned by the Search
        items: A dict of all items returned by the Search

    Args:
        search: The term to search for
        _tags: The list of tags to filter by
    """

    _users: List[User] = None
    _machines: List[Machine] = None
    _teams: List[Team] = None
    _challenges: List[Challenge] = None

    _user_ids: List[int] = None
    _machine_ids: List[int] = None
    _team_ids: List[int] = None
    _challenge_ids: List[int] = None

    _is_resolved: bool = False
    _term: str = None

    @property
    def users(self) -> List[User]:
        if self._users is None:
            self._users = [self._client.get_user(uid) for uid in self._user_ids]
        return self._users

    @property
    def machines(self) -> List[Machine]:
        if self._machines is None:
            self._machines = [self._client.get_machine(uid) for uid in self._machine_ids]
        return self._machines

    @property
    def teams(self) -> List[Team]:
        if self._teams is None:
            self._teams = [self._client.get_team(uid) for uid in self._team_ids]
        return self._teams

    @property
    def challenges(self) -> List[Challenge]:
        if self._challenges is None:
            self._challenges = [self._client.get_challenge(uid) for uid in self._challenge_ids]
        return self._challenges

    @property
    def items(self) -> dict:
        self._is_resolved = True
        return {
            "users": self.users,
            "machines": self.machines,
            "teams": self.teams,
            "challenges": self.challenges
        }

    # noinspection PyStatementEffect
    def __len__(self):
        return len(self._user_ids) + len(self._team_ids) + len(self._machine_ids) + len(self._challenge_ids)

    def __repr__(self):
        return f"<Search '{self._term}': {len(self)} results>"

    def __str__(self):
        return repr(self)

    def __init__(self, search: str, client: htb.HTBClient, _tags=None):
        if _tags is None:
            _tags = []
        self._term = search
        self._client = client
        # Ignoring tags - they seem to currently not work on the API level
        search_data = self._client.do_request("search/fetch?query=" + search)
        self._user_ids = [x['id'] for x in search_data.get("users", [])]
        self._machine_ids = [x['id'] for x in search_data.get("machines", [])]
        self._team_ids = [x['id'] for x in search_data.get("teams", [])]
        self._challenge_ids = [x['id'] for x in search_data.get("challenges", [])]
