import os
from os import getenv
import sys
from pytest import fixture
from hackthebox import HTBClient
from dotenv import load_dotenv
import mock_api

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@fixture(scope="session")
def htb_client() -> HTBClient:
    return HTBClient(email=getenv("HTB_EMAIL"), password=getenv("HTB_PASSWORD"))


@fixture(scope="session")
def mock_htb_client() -> HTBClient:
    mock_api.start_mock_server()
    client = HTBClient(email="user@example.com", password="password", api_base="http://localhost:9000/api/v4/")
    return client
