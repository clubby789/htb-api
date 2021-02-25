import os
from os import getenv
import sys
from pytest import fixture
from hackthebox import HTBClient
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@fixture
def htb_client() -> HTBClient:
    return HTBClient(email=getenv("HTB_EMAIL"), password=getenv("HTB_PASSWORD"))
