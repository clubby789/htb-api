# HackTheBoxPy
[![Run Tests](https://github.com/clubby789/htb-api/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/clubby789/htb-api/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/clubby789/htb-api/branch/master/graph/badge.svg?token=NPoxQPqdyN)](https://codecov.io/gh/clubby789/htb-api)

HackTheBoxPy is an unofficial Python library to interact with the Hack The Box API.


## Install
`python setup.py install`

## Demo
```py
from hackthebox import HTBClient
client = HTBClient(email="user@example.com", password="S3cr3tP455w0rd!")
print(client.user)
```
