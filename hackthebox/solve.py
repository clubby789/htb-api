from . import htb


class Solve:
    _client: "htb.HTBClient" = None
    _item: "htb.HTBObject" = None   # The solved item
    id: int = None
    name: str = None
    date: str = None
    blood: bool = None
    points: int = None

    def __repr__(self):
        return f"<Solve '{self.name}'>"

    def __init__(self, data: dict, client: "htb.HTBClient"):
        self._client = client
        self.date = data['date']
        self.blood = data['first_blood']
        self.id = data['id']
        self.name = data['name']


class MachineSolve(Solve):
    type: str = None   # User/Root

    @property
    async def machine(self):
        if not self._item:
            self._item = await self._client.get_machine(self.id)
        return self._item

    def __init__(self, data: dict, client: "htb.HTBClient"):
        super().__init__(data, client)
        self.type = data['type']


class ChallengeSolve(Solve):
    category: str = None

    @property
    async def challenge(self):
        if not self._item:
            self._item = await self._client.get_challenge(self.id)
        return self._item

    def __init__(self, data: dict, client: "htb.HTBClient"):
        super().__init__(data, client)
        self.category = data['challenge_category']


class EndgameSolve(Solve):
    flag_name: str = None

    @property
    async def endgame(self):
        if not self._item:
            # TODO: Implement endgames
            self._item = await self._client.get_endgame(self.id)
        return self._item

    def __init__(self, data: dict, client: "htb.HTBClient"):
        super().__init__(data, client)
        self.flag_name = data['flag_title']


class FortressSolve(Solve):
    flag_name: str = None

    @property
    async def endgame(self):
        if not self._item:
            # TODO: Implement fortresses
            self._item = await self._client.get_fortress(self.id)
        return self._item

    def __init__(self, data: dict, client: "htb.HTBClient"):
        super().__init__(data, client)
        self.flag_name = data['flag_title']