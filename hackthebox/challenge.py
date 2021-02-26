from . import htb


class Challenge(htb.HTBObject):
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

    # noinspection PyUnresolvedReferences
    def __init__(self, data: dict, client: "HTBClient", summary: bool = False):
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
