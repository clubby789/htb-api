from typing import List

from . import htb
from .solve import MachineSolve, ChallengeSolve, EndgameSolve, FortressSolve, Solve
from .errors import UnknownSolveException


class User(htb.HTBObject):
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
    # noinspection PyUnresolvedReferences
    team: "Team" = None
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
    def activity(self):
        if not self._activity:
            self._activity = []
            solve_list = (self._client.do_request(f"user/profile/activity/{self.id}"))['profile']['activity']
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

    # noinspection PyUnresolvedReferences
    def __init__(self, data: dict, client: "HTBClient", summary: bool = False):
        """Initialise a `Challenge` using API data"""
        self._client = client
        self._detailed_func = client.get_user
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
