import base64
import json
import os
import time
from threading import Thread

from flask import Flask, request, jsonify, Response

from . import static

CORRECT_CHALLENGE = "HTB{a_challenge_flag}"
CORRECT_HASH = "30ea86803e0d85be51599c3a4e422266"
CHALLENGE_CRACKTHIS = {
    "id": 1,
    "name": "Crack This!",
    "description": "Crack the program and get the flag!",
    "category_name": "Reversing",
    "creator_id": 1,
    "creator_name": "Nobody",
    "creator2_id": None,
    "creator2_name": None,
    "retired": True,
    "points": 0,
    "difficulty_chart": {},
    "difficulty": "Hard",
    "solves": 1,
    "authUserSolve": True,
    "likes": 1,
    "dislikes": 1,
    "release_date": "2017-06-29T19:00:00.000000Z",
    "docker": False,
    "docker_ip": None,
    "download": True,
}

CHALLENGE_WEATHERAPP = {
    "id": 196,
    "name": "Weather App",
    "retired": False,
    "difficulty": "Easy",
    "points": "30",
    "difficulty_chart": {},
    "solves": 1,
    "authUserSolve": True,
    "likes": 1,
    "dislikes": 1,
    "description": "A pit of eternal darkness, a mindless journey of abeyance, this feels like a never-ending dream. I think I'm hallucinating with the memories of my past life, it's a reflection of how thought I would have turned out if I had tried enough. A weatherman, I said! Someone my community would look up to, someone who is to be respected. I guess this is my way of telling you that I've been waiting for someone to come and save me. This weather application is notorious for trapping the souls of ambitious weathermen like me. Please defeat the evil bruxa that's operating this website and set me free! 🧙‍♀️",
    "category_name": "Web",
    "creator_id": 95,
    "creator_name": "makelarisjr",
    "creator2_id": 107,
    "creator2_name": "makelaris",
    "download": True,
    "docker": True,
    "docker_ip": "10.0.0.0",
    "docker_port": 1337,
    "release_date": "2021-01-29T20:00:00.000000Z",
}


CHALLENGE_NGINXATSU = {
    "id": 143,
    "name": "nginxatsu",
    "retired": False,
    "difficulty": "Medium",
    "points": "40",
    "difficulty_chart": {},
    "solves": 1,
    "authUserSolve": True,
    "likes": 1,
    "dislikes": 1,
    "description": "Team Seb managed to abduct nginxatsu from Dr. Talin's hospital after he was submitted there for injuries he sustained from a recent duel. Now they've turned him into a nginx config generator, this is so despicable... YOU HAVE TO SAVE HIM!",
    "category_name": "Web",
    "creator_id": 95,
    "creator_name": "makelarisjr",
    "creator2_id": 107,
    "creator2_name": "makelaris",
    "download": True,
    "docker": True,
    "docker_ip": "10.0.0.0",
    "docker_port": 1337,
    "release_date": "2021-01-29T20:00:00.000000Z",
}

CHALLENGE_QUICKR = {
    "id": 119,
    "name": "QuickR",
    "retired": False,
    "difficulty": "Medium",
    "points": "40",
    "difficulty_chart": {},
    "solves": 1,
    "authUserSolve": True,
    "likes": 1,
    "dislikes": 1,
    "description": "Let's see if you're a QuickR soldier as you pretend to be",
    "category_name": "Misc",
    "creator_id": 95,
    "creator_name": "makelarisjr",
    "creator2_id": 107,
    "creator2_name": "makelaris",
    "download": False,
    "docker": True,
    "docker_ip": "10.0.0.0",
    "docker_port": 1337,
    "release_date": "2021-01-29T20:00:00.000000Z",
}

USER_CH4P = {
    "id": 1,
    "name": "ch4p",
    "system_owns": 67,
    "user_owns": 67,
    "user_bloods": 0,
    "system_bloods": 0,
    "points": 1,
    "ranking": 1,
    "rank": "Noob",
    "respects": 1,
    "university": None,
    "university_name": None,
    "description": None,
    "github": None,
    "linkedin": None,
    "twitter": None,
    "website": None,
    "current_rank_progress": None,
    "next_rank": None,
    "next_rank_points": None,
    "rank_ownership": 0.0,
    "rank_requirement": None,
    "country_name": None,
    "team": {},
    "public": True,
}

USER_MAKELARISJR = {
    "id": 95,
    "name": "makelarisjr",
    "system_owns": 67,
    "user_owns": 67,
    "user_bloods": 0,
    "system_bloods": 0,
    "points": 1,
    "ranking": 1,
    "rank": "Noob",
    "respects": 1,
    "university": None,
    "university_name": None,
    "description": None,
    "github": None,
    "linkedin": None,
    "twitter": None,
    "website": None,
    "current_rank_progress": None,
    "next_rank": None,
    "next_rank_points": None,
    "rank_ownership": 0.0,
    "rank_requirement": None,
    "country_name": None,
    "team": {},
    "public": True,
}

USER_MAKELARIS = {
    "id": 107,
    "name": "makelaris",
    "system_owns": 67,
    "user_owns": 67,
    "user_bloods": 0,
    "system_bloods": 0,
    "points": 1,
    "ranking": 1,
    "rank": "Noob",
    "respects": 1,
    "university": None,
    "university_name": None,
    "description": None,
    "github": None,
    "linkedin": None,
    "twitter": None,
    "website": None,
    "current_rank_progress": None,
    "next_rank": None,
    "next_rank_points": None,
    "rank_ownership": 0.0,
    "rank_requirement": None,
    "country_name": None,
    "team": {},
    "public": True,
}

USER_HTBBOT = {
    "id": 16,
    "name": "HTB Bot",
    "system_owns": 67,
    "user_owns": 67,
    "user_bloods": 0,
    "system_bloods": 0,
    "points": 1,
    "ranking": 1,
    "rank": "Noob",
    "respects": 1,
    "university": None,
    "university_name": None,
    "description": None,
    "github": None,
    "linkedin": None,
    "twitter": None,
    "website": None,
    "current_rank_progress": None,
    "next_rank": None,
    "next_rank_points": None,
    "rank_ownership": 0.0,
    "rank_requirement": None,
    "country_name": None,
    "team": {},
    "public": True,
}

USER_ISTARCHEATERS = {
    "id": 272569,
    "name": "IStarCheaters",
    "system_owns": 67,
    "user_owns": 67,
    "user_bloods": 0,
    "system_bloods": 0,
    "points": 1,
    "ranking": 1,
    "rank": "Noob",
    "respects": 1,
    "university": None,
    "university_name": None,
    "description": None,
    "github": None,
    "linkedin": None,
    "twitter": None,
    "website": None,
    "current_rank_progress": None,
    "next_rank": None,
    "next_rank_points": None,
    "rank_ownership": 0.0,
    "rank_requirement": None,
    "country_name": None,
    "team": None,
    "public": True,
}

USER_CLUBBY = {
    "id": 83743,
    "name": "clubby789",
    "server_id": 254,
    "avatar": None,
    "beta_tester": 0,
    "rank_id": 7,
    "onboarding_completed": True,
    "verified": True,
    "can_delete_avatar": True,
    "team": {
        "id": 1709,
        "name": "WinBARs",
    },
    "university": None,
    "hasTeamInvitation": True,
    "subscription_plan": None,
    "user_owns": 1,
    "system_owns": 1,
    "root_owns": 1,
    "user_bloods": 1,
    "system_bloods": 1,
    "root_bloods": 1,
    "points": 1,
    "ranking": 1,
    "rank": "Noob",
    "respects": 1,
    "university_name": None,
    "description": None,
    "github": None,
    "linkedin": None,
    "twitter": None,
    "website": None,
    "current_rank_progress": None,
    "next_rank": None,
    "next_rank_points": None,
    "rank_ownership": 0.0,
    "rank_requirement": None,
    "country_name": None,
    "public": True,
}

USER_CONTENT_CLUBBY = {
    "content": {
        "machines": [
            {
                "id": 219,
                "name": "Obscurity",
                "os": "Linux",
                "machine_avatar": "/storage/avatars/8c606d79541774c87ab0ee5705821323.png",
                "difficulty": "Medium",
                "rating": "4.0",
                "user_owns": 8559,
                "system_owns": 8351,
            },
        ],
        "challenges": [
            {
                "id": 1,
                "name": "QuickR",
                "category": "Misc",
                "likes": 223,
                "dislikes": 7,
            },
            {
                "id": 196,
                "name": "Weather App",
                "category": "Web",
                "likes": 2566,
                "dislikes": 38,
            },
            {
                "id": 1,
                "name": "Crack This!",
                "category": "Reversing",
                "likes": 7,
                "dislikes": 0,
            },
        ],
        "writeups": [
            {
                "id": 779,
                "machine_id": 194,
                "machine_avatar": "/storage/avatars/fd39597e558b1b53e91b9ad9dd9619a5.png",
                "machine_name": "Jarvis",
                "url": "https://clubby789.github.io/hackthebox/jarvis/",
                "likes": 0,
                "dislikes": 0,
                "type": "machine",
            },
        ],
    }
}


USER_EKS = {
    "id": 302,
    "name": "eks",
    "avatar": None,
    "beta_tester": 0,
    "rank_id": 7,
    "onboarding_completed": True,
    "verified": True,
    "can_delete_avatar": True,
    "team": None,
    "university": None,
    "hasTeamInvitation": True,
    "subscription_plan": None,
    "user_owns": 1,
    "system_owns": 1,
    "user_bloods": 1,
    "system_bloods": 1,
    "points": 1,
    "ranking": 1,
    "rank": "Noob",
    "respects": 1,
    "university_name": None,
    "description": None,
    "github": None,
    "linkedin": None,
    "twitter": None,
    "website": None,
    "current_rank_progress": None,
    "next_rank": None,
    "next_rank_points": None,
    "rank_ownership": 0.0,
    "rank_requirement": None,
    "country_name": None,
    "public": True,
}

MACHINE_LAME = {
    "id": 1,
    "name": "Lame",
    "os": "Linux",
    "active": 1,
    "retired": 1,
    "ip": "10.10.10.3",
    "points": 0,
    "static_points": 20,
    "release": "2017-03-14T19:54:51.000000Z",
    "user_owns_count": 1,
    "root_owns_count": 1,
    "free": False,
    "authUserInUserOwns": True,
    "authUserInRootOwns": True,
    "authUserHasReviewed": False,
    "stars": "4.4",
    "difficulty": 26,
    "feedbackForChart": {},
    "difficultyText": "Easy",
    "isCompleted": True,
    "last_reset_time": None,
    "playInfo": {
        "isSpawned": None,
        "isSpawning": None,
        "isActive": False,
        "active_player_count": None,
        "expires_at": None,
    },
    "maker": {
        "id": 1,
        "name": "ch4p",
    },
    "maker2": {
        "id": 1,
        "name": "ch4p",
    },
    "recommended": 0,
    "sp_flag": 0,
    "avatar": None,
    "authUserFirstUserTime": "2Y 5M 17D",
    "authUserFirstRootTime": "2Y 5M 17D",
    "userBlood": {
        "user": {"name": "0x1Nj3cT0R", "id": 22, "avatar": None},
        "created_at": "2017-04-02 23:50:16",
        "blood_difference": "18D 22H 55M",
    },
    "userBloodAvatar": None,
    "rootBlood": {
        "user": {"name": "0x1Nj3cT0R", "id": 22, "avatar": None},
        "created_at": "2017-04-02 23:49:27",
        "blood_difference": "18D 22H 54M",
    },
    "rootBloodAvatar": None,
    "firstUserBloodTime": "18D 22H 55M",
    "firstRootBloodTime": "18D 22H 54M",
}

MACHINE_OBSCURITY = {
    "id": 219,
    "name": "Obscurity",
    "os": "Linux",
    "active": 0,
    "retired": 1,
    "points": 0,
    "static_points": 30,
    "release": "2019-11-30T17:00:00.000000Z",
    "user_owns_count": 8559,
    "root_owns_count": 8351,
    "free": False,
    "authUserInUserOwns": True,
    "authUserInRootOwns": True,
    "authUserHasReviewed": False,
    "stars": "4.0",
    "difficulty": 48,
    "avatar": "/storage/avatars/8c606d79541774c87ab0ee5705821323.png",
    "feedbackForChart": {
        "counterCake": 629,
        "counterVeryEasy": 1089,
        "counterEasy": 2220,
        "counterTooEasy": 2490,
        "counterMedium": 5843,
        "counterBitHard": 1689,
        "counterHard": 1419,
        "counterTooHard": 840,
        "counterExHard": 318,
        "counterBrainFuck": 350,
    },
    "difficultyText": "Medium",
    "isCompleted": True,
    "last_reset_time": "1 year before",
    "playInfo": {
        "isSpawned": False,
        "isSpawning": None,
        "isActive": None,
        "active_player_count": None,
        "expires_at": None,
    },
    "maker": {
        "id": 83743,
        "name": "clubby789",
        "avatar": "/storage/avatars/571a1cebb38673df9a38f5fd5ede9276.png",
        "isRespected": False,
    },
    "maker2": None,
    "authUserFirstUserTime": "1D 0H 35M",
    "authUserFirstRootTime": "1D 1H 56M",
    "userBlood": {
        "user": {
            "name": "sampriti",
            "id": 836,
            "avatar": "/storage/avatars/03d6176149e9fe81c83590dd4e7a5225.png",
        },
        "created_at": "2019-11-30 21:24:12",
        "blood_difference": "0H 24M 12S",
    },
    "userBloodAvatar": "/storage/avatars/03d6176149e9fe81c83590dd4e7a5225.png",
    "rootBlood": {
        "user": {
            "name": "sampriti",
            "id": 836,
            "avatar": "/storage/avatars/03d6176149e9fe81c83590dd4e7a5225.png",
        },
        "created_at": "2019-11-30 21:36:36",
        "blood_difference": "0H 36M 36S",
    },
    "rootBloodAvatar": "/storage/avatars/03d6176149e9fe81c83590dd4e7a5225.png",
    "firstUserBloodTime": "0H 24M 12S",
    "firstRootBloodTime": "0H 36M 36S",
    "recommended": 0,
    "sp_flag": 0,
    "lab_server": None,
}

MACHINE_DRIVER_RA = {
    "avatar": "/storage/avatars/4aee57cc02f0181b22f4ccd43775f7ac.png",
    "expires_at": None,
    "id": 387,
    "isSpawning": None,
    "name": "Driver",
    "voted": None,
    "voting": None,
    "ip": "10.129.145.8",
    "lifespan": 1440,
    "type": "Release Arena",
    "lab_server": "ra_lab",
}

MACHINE_DRIVER_ACTIVE = {
    "avatar": "/storage/avatars/ce42ce9fd28d117b8d6c045aefeb5cdb.png",
    "expires_at": "2022-02-26 22:44:08",
    "id": 387,
    "isSpawning": None,
    "lab_server": "vip_lab",
    "name": "Driver",
    "type": "Free",
    "voted": False,
    "voting": False,
}

MACHINE_DRIVER = {
    "id": 387,
    "name": "Driver",
    "os": "Windows",
    "active": 1,
    "retired": 0,
    "ip": "10.10.11.106",
    "points": 20,
    "static_points": 20,
    "release": "2021-10-02T16:00:00.000000Z",
    "user_owns_count": 9521,
    "root_owns_count": 8313,
    "free": True,
    "authUserInUserOwns": True,
    "authUserInRootOwns": True,
    "authUserHasReviewed": False,
    "stars": "4.7",
    "difficulty": 42,
    "avatar": "/storage/avatars/ce42ce9fd28d117b8d6c045aefeb5cdb.png",
    "feedbackForChart": {
        "counterCake": 470,
        "counterVeryEasy": 731,
        "counterEasy": 2186,
        "counterTooEasy": 2549,
        "counterMedium": 2570,
        "counterBitHard": 847,
        "counterHard": 494,
        "counterTooHard": 161,
        "counterExHard": 42,
        "counterBrainFuck": 117,
    },
    "difficultyText": "Easy",
    "isCompleted": True,
    "last_reset_time": "2 weeks before",
    "playInfo": {
        "isSpawned": True,
        "isSpawning": None,
        "isActive": True,
        "active_player_count": 2,
        "expires_at": "2022-02-26 22:44:08",
    },
    "maker": {
        "id": 13531,
        "name": "MrR3boot",
        "avatar": "/storage/avatars/35b0a38a649c5cf0537bf544451b95fb.png",
        "isRespected": True,
    },
    "maker2": None,
    "authUserFirstUserTime": "3M 16D 6H",
    "authUserFirstRootTime": "3M 16D 6H",
    "userBlood": {
        "user": {
            "name": "Wh04m1",
            "id": 4483,
            "avatar": "/storage/avatars/0fc6d83a6ab0b4f6ce8cd8c8dd5083fe.png",
        },
        "created_at": "2021-10-02 22:21:10",
        "blood_difference": "0H 21M 10S",
    },
    "userBloodAvatar": "/storage/avatars/0fc6d83a6ab0b4f6ce8cd8c8dd5083fe.png",
    "rootBlood": {
        "user": {
            "name": "RealEnox",
            "id": 256488,
            "avatar": "/storage/avatars/656c1c48ce65e2341f887e3c6d3e4436.png",
        },
        "created_at": "2021-10-02 22:29:13",
        "blood_difference": "0H 29M 13S",
    },
    "rootBloodAvatar": "/storage/avatars/656c1c48ce65e2341f887e3c6d3e4436.png",
    "firstUserBloodTime": "0H 21M 10S",
    "firstRootBloodTime": "0H 29M 13S",
    "recommended": 0,
    "sp_flag": 0,
    "lab_server": "vip_lab",
}

ENDGAME_POO = {
    "id": 1,
    "name": "P.O.O.",
    "avatar_url": None,
    "cover_image_url": None,
    "retired": True,
    "vip": True,
    "creators": [
        {
            "id": 302,
            "name": "eks",
        }
    ],
    "points": 0,
    "players_completed": 944,
    "endgame_reset_votes": 0,
    "most_recent_reset": None,
    "entry_points": [],
    "video_url": None,
    "description": None,
    "completion_icon": "fa-chess",
    "completion_text": "Castling",
    "has_user_finished": True,
}

FORTRESS_JET = {
    "id": 1,
    "name": "Jet",
    "image": "",
    "cover_image_url": "",
    "new": False,
    "number_of_flags": 11,
    "user_availability": {"available": False, "code": 0, "message": None},
    "flags": [],
    "company": {"id": 1, "name": None, "description": None, "url": None, "image": None},
    "reset_votes": 0,
    "progress_percent": 0,
    "ip": None,
}

TEAM_WINRARS = {
    "id": 2710,
    "name": "TheWINRaRs",
    "points": 11,
    "motto": None,
    "description": None,
    "country_name": "United Kingdom",
    "country_code": "GB",
    "cover_image_url": None,
    "twitter": None,
    "facebook": None,
    "discord": None,
    "public": True,
    "avatar_url": None,
    "can_delete_avatar": False,
    "captain": {
        "id": 293491,
        "name": "lukevaxhacker",
    },
    "is_respected": False,
    "join_request_sent": False,
}

TEAM_ADMINS = {
    "id": 2710,
    "name": "TheWINRaRs",
    "points": 11,
    "motto": None,
    "description": "",
    "country_name": "Greece",
    "country_code": "GB",
    "cover_image_url": None,
    "twitter": None,
    "facebook": None,
    "discord": None,
    "public": True,
    "avatar_url": None,
    "can_delete_avatar": False,
    "captain": {
        "id": 1,
        "name": "ch4p",
    },
    "is_respected": False,
    "join_request_sent": False,
}

TODO_LIST = {
    "machines": [
        {
            "id": 109,
            "name": "Minion",
            "os": "Windows",
            "points": 0,
            "difficulty": "Insane",
            "avatar": "/storage/avatars/2ed1156a2aaaba7935ebb31d1ffd8ee0.png",
            "user_flag": True,
            "root_flag": True,
            "root_flag_only": False,
            "url": "/machines/Minion",
        },
        {
            "id": 113,
            "name": "Tally",
            "os": "Windows",
            "points": 0,
            "difficulty": "Hard",
            "avatar": "/storage/avatars/72c8ccb9247de82b107cd045528e45a8.png",
            "user_flag": True,
            "root_flag": True,
            "root_flag_only": False,
            "url": "/machines/Tally",
        },
        {
            "id": 114,
            "name": "Jeeves",
            "os": "Windows",
            "points": 0,
            "difficulty": "Medium",
            "avatar": "/storage/avatars/709059a710d3d6ff1ba32bf0729ecbb8.png",
            "user_flag": True,
            "root_flag": True,
            "root_flag_only": False,
            "url": "/machines/Jeeves",
        },
    ],
    "challenges": [],
    "tracks": [],
    "prolabs": [],
}


CONNECTIONS = {
    "status": True,
    "data": {
        "lab": {
            "can_access": True,
            "location_type_friendly": "EU - VIP",
            "assigned_server": {
                "id": 61,
                "friendly_name": "EU VIP 20",
                "current_clients": 3,
                "location": "EU",
            },
        },
        "starting_point": {
            "can_access": True,
            "location_type_friendly": "US - Starting Point VIP",
            "assigned_server": {
                "id": 415,
                "friendly_name": "US StartingPoint VIP 1",
                "current_clients": 40,
                "location": "US",
            },
        },
        "endgames": {
            "can_access": True,
            "location_type_friendly": "EU - Endgame",
            "assigned_server": {
                "id": 37,
                "friendly_name": "EU Endgame 1",
                "current_clients": 1,
                "location": "EU",
            },
        },
        "fortresses": {
            "can_access": True,
            "location_type_friendly": "US - Fortress",
            "assigned_server": {
                "id": 19,
                "friendly_name": "US Fortress 1",
                "current_clients": 6,
                "location": "US",
            },
        },
        "pro_labs": {"can_access": False, "assigned_server": None},
        "release_arena": {
            "can_access": True,
            "assigned_server": {
                "id": 268,
                "friendly_name": "US Release Lab 1",
                "current_clients": 55,
                "location": "US",
            },
            "available": True,
            "location_type_friendly": "US - Release Arena",
            "machine": {
                "id": 444,
                "name": "RouterSpace",
                "avatar_thumb_url": "https://www.hackthebox.com/storage/avatars/4aee57cc02f0181b22f4ccd43775f7ac_thumb.png",
            },
        },
    },
}


has_ratelimited: bool = False

app = Flask(__name__)


@app.route("/api/v4/challenge/list", methods=["GET"])
def list_challenges():
    return jsonify({"challenges": [CHALLENGE_CRACKTHIS for _ in range(30)]})


@app.route("/api/v4/challenge/list/retired", methods=["GET"])
def list_retired_challenges():
    return jsonify({"challenges": [CHALLENGE_CRACKTHIS for _ in range(30)]})


@app.route("/api/v4/challenge/info/<num>", methods=["GET"])
def get_challenge(num):
    num = int(num)
    if num == 1:
        return jsonify({"challenge": CHALLENGE_CRACKTHIS})
    if num == 143:
        return jsonify({"challenge": CHALLENGE_NGINXATSU})
    if num == 119:
        return jsonify({"challenge": CHALLENGE_QUICKR})
    if num == 196:
        return jsonify({"challenge": CHALLENGE_WEATHERAPP})
    return jsonify({"message": "Challenge not found"}), 404


@app.route("/api/v4/challenge/own", methods=["POST"])
def own_challenge():
    if request.json["flag"] == CORRECT_CHALLENGE:
        return jsonify({"message": "Congratulations"})
    else:
        return jsonify({"message": "Incorrect flag"})


@app.route("/api/v4/machine/list")
def list_machines():
    return jsonify({"info": [MACHINE_LAME for _ in range(20)]})


@app.route("/api/v4/machine/active")
def get_active_machine():
    token = request.headers.get("Authorization").split(".")[1]
    token_dict = json.loads(base64.b64decode(token).decode())
    if "no_active" in token_dict:
        return jsonify({"info": None})
    return jsonify({"info": MACHINE_DRIVER_ACTIVE})


@app.route("/api/v4/release_arena/active")
def get_active_ra():
    token = request.headers.get("Authorization").split(".")[1]
    token_dict = json.loads(base64.b64decode(token).decode())
    if "no_active" in token_dict:
        return jsonify({"info": None})
    return jsonify({"info": MACHINE_DRIVER_RA})


@app.route("/api/v4/machine/list/retired")
def list_retired_machines():
    return jsonify({"info": [MACHINE_LAME for _ in range(150)]})


@app.route("/api/v4/machine/own", methods=["POST"])
def own_machine():
    if request.json["flag"] == CORRECT_HASH:
        return jsonify({"message": "Congratulations"})
    else:
        return jsonify({"message": "Incorrect flag!"})


@app.route("/api/v4/machine/profile/<num>")
def get_machine(num):
    num = int(num)
    if num == 1:
        return jsonify({"info": MACHINE_LAME})
    elif num == 387:
        return jsonify({"info": MACHINE_DRIVER})
    elif num == 219:
        return jsonify({"info": MACHINE_OBSCURITY})


@app.route("/api/v4/home/user/todo")
def get_todo():
    return jsonify({"data": TODO_LIST})


@app.route("/api/v4/login", methods=["POST"])
def login():
    otp = request.json["email"] == "otpuser@example.com"
    if request.json["remember"]:
        exp = time.time() + 30 * 24 * 60 * 60
    else:
        exp = time.time() + 100
    token = (
        base64.b64encode(json.dumps({"typ": "JWT", "alg": "RS256"}).encode()).decode()
        + "."
        + base64.b64encode(
            json.dumps(
                {
                    "aud": "0",
                    "jti": "",
                    "iat": 0,
                    "nbf": 0,
                    "exp": exp,
                    "sub": "0",
                    "scopes": [],
                }
            ).encode()
        ).decode()
        + "."
    )
    return jsonify(
        {
            "message": {
                "access_token": token,
                "refresh_token": "FakeToken",
                "is2FAEnabled": otp,
            }
        }
    )


@app.route("/api/v4/2fa/login", methods=["POST"])
def otp_login():
    if request.json["one_time_password"] == "111111":
        return jsonify({"message": "OTP correct"})
    else:
        return jsonify({"message": "OTP wrong"}), 400


@app.route("/api/v4/login/refresh", methods=["POST"])
def refresh():
    token = (
        base64.b64encode(json.dumps({"typ": "JWT", "alg": "RS256"}).encode()).decode()
        + "."
        + base64.b64encode(
            json.dumps(
                {
                    "aud": "0",
                    "jti": "",
                    "iat": 0,
                    "nbf": 0,
                    "exp": time.time() + 100,
                    "sub": "0",
                    "scopes": [],
                }
            ).encode()
        ).decode()
        + "."
    )
    return jsonify({"message": {"access_token": token, "refresh_token": "FakeToken"}})


@app.route("/api/v4/challenge/start", methods=["POST"])
def start_challenge():
    if request.json["challenge_id"] == 143:
        return jsonify(
            {
                "message": "Instance Created!",
                "id": "webnginxatsu-83743",
                "port": 31475,
                "ip": "10.10.10.10",
            }
        )
    else:
        return jsonify({"message": "Incorrect Parameters"})


@app.route("/api/v4/challenge/stop", methods=["POST"])
def stop_challenge():
    return jsonify({"message": "Container Stopped"})


@app.route("/api/v4/endgame/<_num>/flag", methods=["POST"])
def submit_endgame_flag(_num):
    if request.json["flag"] == CORRECT_HASH:
        return jsonify({"message": "Congratulations"})
    else:
        return jsonify({"message": "Wrong flag"})


@app.route("/api/v4/endgames")
def get_endgames():
    return jsonify({"data": [ENDGAME_POO for _ in range(5)]})


@app.route("/api/v4/endgame/<num>")
def get_endgame(num):
    num = int(num)
    if num == 1:
        return jsonify({"data": ENDGAME_POO})
    return jsonify({"message": "No results for this endgame"}), 404


@app.route("/api/v4/fortresses")
def list_fortresses():
    return jsonify({"data": {str(i): FORTRESS_JET for i in range(3)}})


@app.route("/api/v4/fortress/<num>")
def get_fortress(num):
    num = int(num)
    if num == 1:
        return jsonify({"data": FORTRESS_JET})


@app.route("/api/v4/fortress/<_num>/flag", methods=["POST"])
def submit_fortress_flag(_num):
    if request.json["flag"] == CORRECT_HASH:
        return jsonify({"message": "Congratulations"})
    else:
        return jsonify({"message": "Wrong flag"})


@app.route("/api/v4/challenge/download/<_num>")
def download_challenge(_num):
    return Response(b"Not really zip data", mimetype="application/zip")


@app.route("/api/v4/rankings/users")
def get_user_list():
    return jsonify({"data": [USER_CLUBBY for _ in range(100)]})


@app.route("/api/v4/rankings/teams")
def get_team_list():
    return jsonify({"data": [{"id": 100, "name": "schmangs"} for _ in range(100)]})


@app.route("/api/v4/rankings/countries")
def get_country_list():
    c = {
        "id": 1,
        "country": "UK",
        "name": "United Kingdom",
        "rank": 1,
        "points": 1,
        "members": 1,
        "user_owns": 1,
        "root_owns": 1,
        "challenge_owns": 1,
        "user_bloods": 1,
        "root_bloods": 1,
        "challenge_bloods": 1,
        "fortress": 1,
        "endgame": 1,
    }
    return jsonify({"data": [c for _ in range(100)]})


@app.route("/api/v4/rankings/universities")
def get_uni_list():
    u = {
        "id": 1,
        "name": "Uni Uni",
        "rank": 1,
        "points": 1,
        "students": 1,
        "user_owns": 1,
        "root_owns": 1,
        "challenge_owns": 1,
        "user_bloods": 1,
        "root_bloods": 1,
        "challenge_bloods": 1,
        "fortress": 1,
        "endgame": 1,
    }
    return jsonify({"data": [u for _ in range(100)]})


@app.route("/api/v4/team/info/<tid>")
def get_team(tid):
    tid = int(tid)
    if tid == 21:
        return jsonify(TEAM_ADMINS)
    if tid == 2710:
        return jsonify(TEAM_WINRARS)
    return jsonify({"message": "No results for this team"}), 404


@app.route("/api/v4/team/stats/owns/<_tid>")
def get_team_owns(_tid):
    return jsonify({"rank": 1})


@app.route("/api/v4/user/profile/basic/<uid>")
def get_basic_profile(uid):
    uid = int(uid)
    if uid == 1:
        return jsonify({"profile": USER_CH4P})
    if uid == 16:
        return jsonify({"profile": USER_HTBBOT})
    if uid == 95:
        return jsonify({"profile": USER_MAKELARISJR})
    if uid == 107:
        return jsonify({"profile": USER_MAKELARIS})
    if uid == 302:
        return jsonify({"profile": USER_EKS})
    if uid == 272569:
        return jsonify({"profile": USER_ISTARCHEATERS})
    if uid == 83743:
        return jsonify({"profile": USER_CLUBBY})
    return jsonify({"message": "No results for this user"}), 404


@app.route("/api/v4/user/profile/activity/<_uid>")
def get_user_activity(_uid):
    return jsonify({"profile": {"activity": []}})


@app.route("/api/v4/user/profile/content/<uid>")
def get_content(uid):
    uid = int(uid)
    if uid == 83743:
        return jsonify({"profile": USER_CONTENT_CLUBBY})


@app.route("/api/v4/user/info")
def get_own_user():
    return jsonify({"info": USER_CLUBBY})


@app.route("/api/v4/search/fetch")
def search():
    return jsonify(
        {"challenges": [], "machines": [MACHINE_LAME], "teams": [], "users": []}
    )


@app.route("/api/v4/connections")
def connections():
    return jsonify(CONNECTIONS)


@app.route("/api/v4/connections/servers")
def get_vpn_servers():
    product = request.args.get("product")
    if product == "labs":
        return jsonify(static.ALL_LABS)
    elif product == "release_arena":
        return jsonify(static.ALL_RA)
    raise


@app.route("/api/v4/connections/servers/switch/<sid>", methods=["POST"])
def switch_vpn(sid):
    token = request.headers.get("Authorization").split(".")[1]
    token_dict = json.loads(base64.b64decode(token).decode())
    if "has_active_machine" in token_dict:
        return jsonify(
            {
                "status": False,
                "message": "You must stop your active machine before switching VPN",
            }
        )
    return jsonify(
        {
            "status": True,
            "message": "VPN Server switched",
            "data": {
                "id": sid,
                "friendly_name": "EU Free 2",
                "current_clients": 64,
                "location": "EU",
            },
        }
    )


@app.route("/api/v4/vm/reset", methods=["POST"])
def reset_box():
    token = request.headers.get("Authorization").split(".")[1]
    token_dict = json.loads(base64.b64decode(token).decode())
    if "too_many_resets" in token_dict:
        return (
            jsonify({"message": "Too many reset machine attempts. Try again later!"}),
            400,
        )
    box_id = request.json["machine_id"]
    return jsonify({"message": "Hancliffe will be reset in 1 minute."})


@app.route("/api/v4/release_arena/reset", methods=["POST"])
def reset_ra():
    token = request.headers.get("Authorization").split(".")[1]
    token_dict = json.loads(base64.b64decode(token).decode())
    if "too_many_resets" in token_dict:
        return (
            jsonify(
                {
                    "success": 0,
                    "message": "You must wait 1 minute between Machine actions.",
                }
            ),
            400,
        )
    return jsonify({"success": 1, "message": "Machine reset!"})


@app.before_request
def ratelimit():
    global has_ratelimited
    if not has_ratelimited:
        has_ratelimited = True
        return "Wait", 429
    return None


def start_server(port: int):
    os.environ["WERKZEUG_RUN_MAIN"] = "true"
    thread = Thread(target=app.run, args=("0.0.0.0", port), daemon=True)
    thread.start()
