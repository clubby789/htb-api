PyHackTheBox
==================

``pyhackthebox`` is an unofficial Python library designed to automate
accessing the Hack The Box API.

Getting Started
---------------
Setting up an API connection::

    from hackthebox import HTBClient
    client = HTBClient(email="user@example.com", password="S3cr3tP455w0rd!", otp="123456")
    print(client.user)

Getting a challenge::

    client.get_challenge(200)
    print(challenge.name)

Searching for a user::

    results = client.search("g0blin")
    print(results.users)


Module Index
---------------

.. toctree::
    :maxdepth: 3
    :glob:

    htb
    challenge
    machine
    fortress
    endgame
    leaderboard
    team
    user
    search
    errors
    solve
    vpn
