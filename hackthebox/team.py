from . import htb


class Team(htb.HTBObject):
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
    _captain: "User" = None
    is_respected: bool
    join_request_sent: bool
    _ranking: int = None
    _captain_id: int = None

    def __repr__(self):
        return f"<Team '{self.name}'>"

    def __init__(self, data: dict, client: htb.HTBClient, summary: bool = False):
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
            self._captain_id = data['captain']['id']
            self.is_respected = data['is_respected']
            self.join_request_sent = data['join_request_sent']

    @property
    async def ranking(self) -> int:
        if not self._ranking:
            data = await self._client.do_request(f"team/stats/owns/{self.id}")
            self._ranking = data['rank']
        return self._ranking

    @property
    async def captain(self) -> "User":
        if not self._captain:
            self._captain = await self._client.get_user(self._captain_id)
        return self._captain
