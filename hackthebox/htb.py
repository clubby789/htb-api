from __future__ import annotations
from typing import List, Callable
import base64
import json
import time
import os

import requests
import aiohttp

from .constants import API_BASE, USER_AGENT
from .solve import Solve, MachineSolve, EndgameSolve, ChallengeSolve, FortressSolve
from .errors import UnknownSolveException, AuthenticationException


if os.name == 'nt':
    # https://github.com/aio-libs/aiohttp/issues/4324#issuecomment-733884349
    from functools import wraps
    # noinspection PyProtectedMember
    from asyncio.proactor_events import _ProactorBasePipeTransport

    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise
        return wrapper
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


def check_expired_jwt(token: str) -> bool:
    payload = base64.b64decode(token.split('.')[1]).decode()
    if time.time() > json.loads(payload)['exp']:
        return True
    else:
        return False


class HTBClient:
    _user: User = None
    _access_token: str = None
    _refresh_token: str = None

    def refresh_access_token(self):
        headers = {"User-Agent": USER_AGENT}
        r = requests.post(API_BASE + "login/refresh", json={
                "refresh_token": self._refresh_token
            }, headers=headers)
        data = r.json()['message']
        self._access_token = data['access_token']
        self._refresh_token = data['refresh_token']

    async def do_request(self, endpoint, json_data=None, data=None, authorized=True) -> dict:
        headers = {"User-Agent": USER_AGENT}
        if authorized:
            if check_expired_jwt(self._access_token):
                self.refresh_access_token()
            headers['Authorization'] = "Bearer " + self._access_token
        async with aiohttp.ClientSession() as session:
            if not json_data and not data:
                async with session.get(API_BASE + endpoint, headers=headers) as r:
                    return await r.json()
            else:
                async with session.post(API_BASE + endpoint, json=json_data, data=data) as r:
                    return await r.json()

    def do_synchronous_request(self, endpoint, json_data=None, data=None, authorized=True) -> dict:
        headers = {"User-Agent": USER_AGENT}
        if authorized:
            if check_expired_jwt(self._access_token):
                self.refresh_access_token()
            headers['Authorization'] = "Bearer " + self._access_token
        if not json_data and not data:
            r = requests.get(API_BASE + endpoint, headers=headers)
        else:
            r = requests.post(API_BASE + endpoint, json=json_data, data=data, headers=headers)
        return r.json()

    def __init__(self, password=None, email=None):
        if not password and not email:
            print("Must give an authentication method")
            raise AuthenticationException
        elif password and not email:
            print("Missing email")
            raise AuthenticationException
        elif email and not password:
            print("Missing password")
            raise AuthenticationException
        else:
            data = self.do_synchronous_request("login", json_data={
                "email": email, "password": password
            }, authorized=False)
            self._access_token = data['message']['access_token']
            self._refresh_token = data['message']['access_token']

    async def get_machine(self, machine_id: int) -> Machine:
        data = (await self.do_request(f"machine/profile/{machine_id}"))['info']
        return Machine(data, self)

    async def get_synchronous_machine(self, machine_id: int) -> Machine:
        data = self.do_synchronous_request(f"machine/profile/{machine_id}")['info']
        return Machine(data, self)

    async def get_machines(self, limit: int = None, retired: bool = False) -> List[Machine]:
        if not retired:
            data = (await self.do_request("machine/list"))['info'][:limit]
        else:
            data = (await self.do_request("machine/list/retired"))['info'][:limit]
        return [Machine(m, self, summary=True) for m in data]

    async def get_challenge(self, challenge_id: int) -> Challenge:
        data = (await self.do_request(f"challenge/info/{challenge_id}"))['challenge']
        return Challenge(data, self)

    def get_synchronous_challenge(self, challenge_id: int) -> Challenge:
        data = self.do_synchronous_request(f"challenge/info/{challenge_id}")['challenge']
        return Challenge(data, self)

    async def get_challenges(self, limit=None, retired=False) -> List[Challenge]:
        if retired:
            data = await self.do_request("challenge/list/retired")
        else:
            data = await self.do_request("challenge/list")
        challenges = []
        for challenge in data['challenges'][:limit]:
            challenges.append(Challenge(challenge, self, summary=True))
        return challenges

    async def get_user(self, user_id: int) -> User:
        data = (await self.do_request(f"user/profile/basic/{user_id}"))['profile']
        return User(data, self)

    def get_synchronous_user(self, user_id: int) -> User:
        data = self.do_synchronous_request(f"user/profile/basic/{user_id}")['profile']
        return User(data, self)

    async def get_team(self, team_id: int) -> Team:
        data = await self.do_request(f"team/info/{team_id}")
        return Team(data, self)

    def get_synchronous_team(self, team_id: int) -> Team:
        data = self.do_synchronous_request(f"team/info/{team_id}")
        return Team(data, self)

    @property
    async def user(self):
        if not self._user:
            uid = (await self.do_request("user/info"))['info']['id']
            self._user = await self.get_user(uid)
        return self._user


class HTBObject:
    # Parent class of all other objects
    _client: HTBClient
    # Attributes not fetched by a summary
    _detailed_attributes: List[str]
    _detailed_func: Callable
    id: int

    def __getattr__(self, item):
        # Missing items because of summary
        if item in self._detailed_attributes:
            new_obj = self._detailed_func(self.id)
            for attr in self._detailed_attributes:
                setattr(self, attr, getattr(new_obj, attr))
            return getattr(self, item)
        else:
            raise AttributeError


class Challenge(HTBObject):
    name: str = None
    retired: bool = None
    difficulty: str = None
    avg_difficulty: int = None
    points: int = None
    difficulty_ratings = None
    solves: int = None
    likes: int = None
    dislikes: int = None
    release_data: str = None
    isCompleted: bool = None
    solved: bool = None
    is_liked: bool = None
    is_disliked: bool = None
    has_download: bool = None
    has_docker: bool = None
    recommended: bool = None

    _detailed_attributes = ('description', 'category', 'author_id', 'author_name', 'has_download', 'has_docker')
    description: str
    category_id: int
    category: str
    author_id: int
    author_name: str
    has_download: bool
    has_docker: bool

    def __repr__(self):
        return f"<Challenge '{self.name}'>"

    def __init__(self, data: dict, client: HTBClient, summary: bool = False):
        """Initialise a `Challenge` using API data"""
        self._client = client
        self._detailed_func = client.get_synchronous_challenge
        self.id = data['id']
        self.name = data['name']
        self.retired = bool(data['retired'])
        self.points = int(data['points'])
        self.difficulty_ratings = data['difficulty_chart']
        self.solves = data['solves']
        self.solved = data['authUserSolve']
        self.likes = data['likes']
        self.dislikes = data['dislikes']
        if not summary:
            self.description = data['description']
            self.category = data['category_name']
            self.author_id = data['creator_id']
            self.author_name = data['creator_name']
            self.has_download = data['download']
            self.has_docker = data['docker']


class Team(HTBObject):
    name: str = None

    _detailed_attributes = ('points', 'motto', 'description', 'country_name', 'avatar_url', 'cover_image_url',
                            'twitter', 'facebook', 'discord', 'public', 'can_delete_avatar', 'captain',
                            'is_respected', 'join_request_sent')
    points: int
    motto: str
    description: str
    country_name: str
    avatar_url: str
    cover_image_url: str
    twitter: str
    facebook: str
    discord: str
    public: bool
    can_delete_avatar: bool
    captain: User
    _captain: User
    is_respected: bool
    join_request_sent: bool
    _ranking: int = None
    _captain_id: int = None

    def __repr__(self):
        return f"<Team '{self.name}'>"

    def __init__(self, data: dict, client: HTBClient, summary: bool = False):
        self._client = client
        self._detailed_func = client.get_synchronous_team
        self.id = data['id']
        self.name = data['name']
        if not summary:
            self.points = data['points']
            self.motto = data['motto']
            self.description = data['description']
            self.country_name = data['country_name']
            self.avatar_url = data['avatar_url']
            self.cover_image_url = data['cover_image_url']
            self.twitter = data['twitter']
            self.facebook = data['facebook']
            self.discord = data['facebook']
            self.public = data['public']
            self.can_delete_avatar = data['can_delete_avatar']
            self._captain_id = data['captain']
            self.is_respected = data['is_respected']
            self.join_request_sent = data['join_request_sent']

    @property
    async def ranking(self) -> int:
        if not self._ranking:
            data = await self._client.do_request(f"team/stats/owns/{self.id}")
            self._ranking = data['rank']
        return self._ranking

    @property
    async def captain(self) -> User:
        if not self._captain:
            self._captain = await self._client.get_user(self._captain_id)
        return self._captain


class User(HTBObject):
    name: str = None
    avatar: str = None
    ranking: int = None
    points: int = None
    root_owns: int = None
    user_owns: int = None
    root_bloods: int = None
    user_bloods: int = None
    rank_name: str = None
    country_name: str = None
    team: Team = None
    public: bool = None

    _detailed_attributes = ('timezone', 'vip', 'vip_plus', 'respects', 'university', 'university_name', 'description',
                            'github', 'linkedin', 'twitter', 'website', 'respected', 'followed', 'rank_id',
                            'rank_progress', 'next_rank', 'next_rank_points', 'rank_ownership', 'rank_requirement')
    timezone: str = None
    vip: bool = None
    vip_plus: bool = None
    respects: int = None
    # TODO: University object
    university = None
    university_name: str = None
    description: str = None
    github: str = None
    linkedin: str = None
    twitter: str = None
    website: str = None
    respected: bool = None
    followed: bool = None
    rank_id: int = None
    rank_progress: int = None
    next_rank: str = None
    next_rank_points: int = None
    rank_ownership: float = None
    rank_requirement: int = None

    _activity: List[Solve] = None

    @property
    async def activity(self):
        if not self._activity:
            self._activity = []
            solve_list = (await self._client.do_request(f"user/profile/activity/{self.id}"))['profile']['activity']
            for solve_item in solve_list:
                solve_type = solve_item['object_type']
                if solve_type == 'machine':
                    self._activity.append(MachineSolve(solve_item, self._client))
                elif solve_type == 'challenge':
                    self._activity.append(ChallengeSolve(solve_item, self._client))
                elif solve_type == 'endgame':
                    self._activity.append(EndgameSolve(solve_item, self._client))
                elif solve_type == 'fortress':
                    self._activity.append(FortressSolve(solve_item, self._client))
                else:
                    print(solve_item)
                    raise UnknownSolveException
        return self._activity

    def __repr__(self):
        return f"<User '{self.name}'>"

    def __init__(self, data: dict, client: HTBClient, summary: bool = False):
        """Initialise a `Challenge` using API data"""
        self._client = client
        self._detailed_func = client.get_synchronous_user
        self.id = data['id']
        self.name = data['name']
        self.user_owns = data['user_owns']
        self.points = data['points']
        self.country_name = data['country_name']
        self.team = data['team']
        self.public = bool(data['public'])
        if summary:
            self.ranking = data['rank']
            self.root_owns = data['root_owns']
            self.user_bloods = data['user_bloods_count']
            self.root_bloods = data['root_bloods_count']
            self.rank_name = data['rank_text']
        else:
            self.ranking = data['ranking']
            self.root_owns = data['system_owns']
            self.user_bloods = data['user_bloods']
            self.root_bloods = data['system_bloods']
            self.rank_name = data['rank']

            self.respects = data['respects']
            self.university = data['university']
            self.university_name = data['university_name']
            self.description = data['description']
            self.github = data['github']
            self.linkedin = data['linkedin']
            self.twitter = data['twitter']
            self.website = data['website']
            self.respected = data.get('isRespected', False)
            self.followed = data.get('isFollowed', False)
            self.rank_progress = data['current_rank_progress']
            self.next_rank = data['next_rank']
            self.next_rank_points = data['next_rank_points']
            self.rank_ownership = float(data['rank_ownership'])
            self.rank_requirement = data['rank_requirement']


class Machine(HTBObject):
    name: str = None
    os: str = None
    points: int = None
    release_date: str = None
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
                            'root_blood', 'user_blood_time', 'root_blood_time')
    active: bool = None
    retired: bool = None
    difficulty_number: int = None
    completed: bool = None
    user_own_time: str = None
    root_own_time: str = None
    user_blood: MachineSolve = None
    root_blood: MachineSolve = None
    user_blood_time: str = None
    root_blood_time: str = None

    _authors: List[User] = None
    _author_ids: List[int] = None

    @property
    async def authors(self) -> List[User]:
        if not self._authors:
            self._authors = []
            for uid in self._author_ids:
                self._authors.append(await self._client.get_user(uid))
        return self._authors

    def __init__(self, data: dict, client: HTBClient, summary: bool = False):
        self._client = client
        self._detailed_func = client.get_synchronous_machine
        self.id = data['id']
        self.name = data['name']
        self.os = data['os']
        self.points = data['points']
        self.release_date = data['release']
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
            self.user_own_time = data['authUserFirstUserTime']
            self.root_own_time = data['authUserFirstRootTime']
            if data['userBlood']:
                user_blood_data = {
                    "date": data['userBlood']['created_at'],
                    "first_blood": True,
                    "id": data['id'],
                    "name": data['name'],
                    "type": "user"
                }
                self.user_blood = MachineSolve(user_blood_data, self._client)
                self.user_blood_time = data['userBlood']['blood_difference']
            if data['rootBlood']:
                user_blood_data = {
                    "date": data['rootBlood']['created_at'],
                    "first_blood": True,
                    "id": data['id'],
                    "name": data['name'],
                    "type": "root"
                }
                self.root_blood = MachineSolve(user_blood_data, self._client)
                self.root_blood_time = data['rootBlood']['blood_difference']
