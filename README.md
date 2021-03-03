# PyHackTheBox
[![Run Tests](https://github.com/clubby789/htb-api/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/clubby789/htb-api/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/clubby789/htb-api/branch/master/graph/badge.svg?token=NPoxQPqdyN)](https://codecov.io/gh/clubby789/htb-api)
[![Documentation Status](https://readthedocs.org/projects/pyhackthebox/badge/?version=latest)](https://pyhackthebox.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/PyHackTheBox.svg)](https://badge.fury.io/py/PyHackTheBox)

PyHackTheBox is an unofficial Python library to interact with the Hack The Box API.


## Install
```bash
$ pip install pyhackthebox
```

## Demo
```py
from hackthebox import HTBClient
# Create an API connection
client = HTBClient(email="user@example.com", password="S3cr3tP455w0rd!")
# Print the User associated with the client
print(client.user)
```

## Documentation

The documentation is available [here](https://pyhackthebox.readthedocs.io/en/latest/).

## Current Features
- Logging into the API (and automatically refreshing access tokens)
- Challenges, Machines, Fortresses and Endgames
  * Getting details
  * Viewing authors
  * Viewing first bloods
  * Submitting flags 
- Searching Users, Challenges, Machines and Teams
- Spawning and stopping Challenge instances
- Retrieving user activity
- Viewing Hall(s) of Fame (Top 100, VIP, Team and University Leaderboards)
