from __future__ import annotations
from typing import List, Callable
import base64
import json
import time
import os

import requests
import aiohttp

from .constants import API_BASE, USER_AGENT
from .errors import AuthenticationException

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
    # noinspection PyUnresolvedReferences
    _user: "User" = None
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

    # noinspection PyUnresolvedReferences
    async def get_machine(self, machine_id: int) -> "Machine":
        from .machine import Machine
        data = (await self.do_request(f"machine/profile/{machine_id}"))['info']
        return Machine(data, self)

    # noinspection PyUnresolvedReferences
    async def get_synchronous_machine(self, machine_id: int) -> "Machine":
        from .machine import Machine
        data = self.do_synchronous_request(f"machine/profile/{machine_id}")['info']
        return Machine(data, self)

    # noinspection PyUnresolvedReferences
    async def get_machines(self, limit: int = None, retired: bool = False) -> List["Machine"]:
        from .machine import Machine
        if not retired:
            data = (await self.do_request("machine/list"))['info'][:limit]
        else:
            data = (await self.do_request("machine/list/retired"))['info'][:limit]
        return [Machine(m, self, summary=True) for m in data]

    # noinspection PyUnresolvedReferences
    async def get_challenge(self, challenge_id: int) -> "Challenge":
        from .challenge import Challenge
        data = (await self.do_request(f"challenge/info/{challenge_id}"))['challenge']
        return Challenge(data, self)

    # noinspection PyUnresolvedReferences
    def get_synchronous_challenge(self, challenge_id: int) -> "Challenge":
        from .challenge import Challenge
        data = self.do_synchronous_request(f"challenge/info/{challenge_id}")['challenge']
        return Challenge(data, self)

    # noinspection PyUnresolvedReferences
    async def get_challenges(self, limit=None, retired=False) -> List["Challenge"]:
        from .challenge import Challenge
        if retired:
            data = await self.do_request("challenge/list/retired")
        else:
            data = await self.do_request("challenge/list")
        challenges = []
        for challenge in data['challenges'][:limit]:
            challenges.append(Challenge(challenge, self, summary=True))
        return challenges

    # noinspection PyUnresolvedReferences
    async def get_user(self, user_id: int) -> "User":
        from .user import User
        data = (await self.do_request(f"user/profile/basic/{user_id}"))['profile']
        return User(data, self)

    # noinspection PyUnresolvedReferences
    def get_synchronous_user(self, user_id: int) -> "User":
        from .user import User
        data = self.do_synchronous_request(f"user/profile/basic/{user_id}")['profile']
        return User(data, self)

    # noinspection PyUnresolvedReferences
    async def get_team(self, team_id: int) -> "Team":
        from .team import Team
        data = await self.do_request(f"team/info/{team_id}")
        return Team(data, self)

    # noinspection PyUnresolvedReferences
    def get_synchronous_team(self, team_id: int) -> "Team":
        from .team import Team
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
