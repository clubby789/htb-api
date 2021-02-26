# HackTheBoxPy

HackTheBoxPy is an unofficial Python library to interact with the Hack The Box API.

## Install
`python setup.py install`

## Demo
```py
from hackthebox import HTBClient
client = HTBClient(email="user@example.com", password="S3cr3tP455w0rd!")
print(client.user)
```
