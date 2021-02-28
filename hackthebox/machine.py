from typing import List
import dateutil.parser
from datetime import datetime, timedelta

from . import htb
from .solve import MachineSolve
from .errors import IncorrectArgumentException, IncorrectFlagException
from .utils import parse_delta


class Machine(htb.HTBObject):
    """ The class representing Hack The Box machines

    Attributes:
        name: The Machine name
        os: The name of the operating system
        points: The points awarded for completion
        release_date: The date the Machine was released
        user_owns: The number of user owns the Machine has
        root_owns: The number of root owns the Machine has
        free: Whethere the Machine is available on free servers
        user_owned: Whether the active User has owned the Machine's user account
        root_owned: Whether the active User has owned the Machine's user account
        reviewed: Whether the active User has reviewed the Machine
        stars: The average star rating of the Machine
        avatar: The relative URL of the Machine avatar
        difficulty: The difficulty of the machine

        active: Whether the Machine is active
        retired: Whether the Machine is retired
        avg_difficulty: The average numeric difficulty of the Machine
        completed: Whether the active User has completed the Machine
         :noindex: user_own_time: How long the active User took to own user
         :noindex: root_own_time: How long the active User took to own root
        user_blood: The Solve of the Machine's first user blood
        root_blood: The Solve of the Machine's first root blood
        user_own_time: How long the first User took to own user
        root_own_time: How long the first User took to own root
        difficulty_ratings: A dict of difficulty ratings given
    """
    name: str = None
    os: str = None
    points: int = None
    release_date: datetime = None
    user_owns: int = None
    root_owns: int = None
    free: bool = None
    user_owned: bool = None
    root_owned: bool = None
    reviewed: bool = None
    stars: float = None
    avatar: str = None
    difficulty: str = None

    _detailed_attributes = ('active', 'retired', 'user_own_time', 'root_own_time', 'user_blood',
                            'root_blood', 'user_blood_time', 'root_blood_time', 'difficulty_ratings')
    active: bool = None
    retired: bool = None
    avg_difficulty: int = None
    completed: bool = None
    user_own_time: timedelta = None
    root_own_time: timedelta = None
    user_blood: MachineSolve = None
    root_blood: MachineSolve = None
    user_blood_time: timedelta = None
    root_blood_time: timedelta = None
    difficulty_ratings: dict = None

    # noinspection PyUnresolvedReferences
    _authors: List["User"] = None
    _author_ids: List[int] = None

    def submit(self, flag: str, difficulty: int):
        """ Submits a flag for a Machine

        Args:
            flag: The flag for the Machine
            difficulty: A rating between 10 and 100 of the Machine difficulty

        """
        if difficulty < 10 or difficulty > 100 or difficulty % 10 != 0:
            raise IncorrectArgumentException

        submission = self._client.do_request("machine/own", json_data={
            "flag": flag,
            "id": self.id,
            "difficulty": difficulty
        })
        if submission['message'] == "Incorrect flag!":
            raise IncorrectFlagException
        return True

    # noinspection PyUnresolvedReferences
    @property
    def authors(self) -> List["User"]:
        """Fetch the author(s) of the Machine

        Returns: List of User

        """
        if not self._authors:
            self._authors = []
            for uid in self._author_ids:
                self._authors.append(self._client.get_user(uid))
        return self._authors

    def __repr__(self):
        return f"<Machine '{self.name}'>"

    def __init__(self, data: dict, client: htb.HTBClient, summary: bool = False):
        self._client = client
        self._detailed_func = client.get_machine
        self.id = data['id']
        self.name = data['name']
        self.os = data['os']
        self.points = data['points']
        self.release_date = dateutil.parser.parse(data['release'])
        self.user_owns = data['user_owns_count']
        self.root_owns = data['root_owns_count']
        self.user_owned = data['authUserInUserOwns']
        self.root_owned = data['authUserInRootOwns']
        self.reviewed = data['authUserHasReviewed']
        self.stars = float(data['stars'])
        self.avatar = data['avatar']
        self.difficulty = data['difficultyText']
        self.free = data['free']
        self._author_ids = [data['maker']['id']]
        if data['maker2']:
            self._author_ids.append(data['maker2']['id'])
        if not summary:
            self.active = bool(data['active'])
            self.retired = bool(data['retired'])
            self.user_own_time = parse_delta(data['authUserFirstUserTime'])
            self.root_own_time = parse_delta(data['authUserFirstRootTime'])
            self.difficulty_ratings = data['feedbackForChart']
            if data['userBlood']:
                user_blood_data = {
                    "date": dateutil.parser.parse(data['userBlood']['created_at']),
                    "first_blood": True,
                    "id": data['id'],
                    "name": data['name'],
                    "type": "user"
                }
                self.user_blood = MachineSolve(user_blood_data, self._client)
                self.user_blood_time = parse_delta(data['userBlood']['blood_difference'])
            if data['rootBlood']:
                user_blood_data = {
                    "date": dateutil.parser.parse(data['rootBlood']['created_at']),
                    "first_blood": True,
                    "id": data['id'],
                    "name": data['name'],
                    "type": "root"
                }
                self.root_blood = MachineSolve(user_blood_data, self._client)
                self.root_blood_time = parse_delta(data['rootBlood']['blood_difference'])
        else:
            self._is_summary = True
