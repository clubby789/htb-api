from __future__ import annotations  # 'Circular dependencies' in the typing
from typing import List, Callable
import base64
import json
import time

import requests

from .constants import API_BASE, USER_AGENT


def check_expired_jwt(token: str) -> bool:
    payload = base64.b64decode(token.split('.')[1]).decode()
    if time.time() > json.loads(payload)['exp']:
        return True
    else:
        return False


class HTBClient:
    username: str = None
    _access_token: str = None
    _refresh_token: str = None

    # TODO: Handle token expiry
    # Add a decorator to every API function to check?

    def _do_request(self, endpoint, json_data=None, data=None, authorized=True) -> dict:
        headers = {"User-Agent": USER_AGENT}
        if authorized:
            if check_expired_jwt(self._access_token):
                r = requests.post(API_BASE + "login/refresh", json={
                    "refresh_token": self._refresh_token
                }, headers=headers)
                data = r.json()['message']
                self._access_token = data['access_token']
                self._refresh_token = data['refresh_token']
            headers['Authorization'] = "Bearer " + self._access_token
        if not json_data and not data:
            r = requests.get(API_BASE + endpoint, headers=headers)
        else:
            r = requests.post(API_BASE + endpoint, json=json_data, data=data, headers=headers)
        return r.json()

    def __init__(self, username=None, password=None, email=None):
        if username:
            self.username = username
        if not password and not email:
            print("Must give an authentication method")
            raise Exception
        elif password and not email:
            print("Missing email")
            raise Exception
        elif email and not password:
            print("Missing password")
            raise Exception
        else:
            data = self._do_request("login", json_data={
                "email": email, "password": password
            }, authorized=False)
            self._access_token = data['message']['access_token']
            self._refresh_token = data['message']['access_token']

    def get_challenge(self, challenge_id: int) -> 'Challenge':
        data = self._do_request(f"challenge/info/{challenge_id}")['challenge']
        return Challenge(data, self)

    def get_challenges(self, limit=None, retired=False) -> List['Challenge']:
        if retired:
            data = self._do_request("challenge/list/retired")
        else:
            data = self._do_request("challenge/list")
        challenges = []
        for challenge in data['challenges'][:limit]:
            challenges.append(Challenge(challenge, self, summary=True))
        return challenges


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
    _detailed_attributes = ('description', 'category', 'author_id', 'author_name', 'has_download', 'has_docker')
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

    description: str
    category_id: int
    category: str
    author_id: int
    author_name: str
    has_download: bool
    has_docker: bool

    def __init__(self, data: dict, client: HTBClient, summary: bool = False):
        """Initialise a `Challenge` using API data"""
        self._client = client
        self._detailed_func = client.get_challenge
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
