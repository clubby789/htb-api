import os
import sys


from pytest import fixture
from hackthebox import HTBClient
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@fixture(scope="session")
def mock_htb_client() -> HTBClient:
    import random
    from mock_api.app import start_server
    import time
    port = random.randint(1024, 65535)
    start_server(port)
    # Wait for server thread to start
    time.sleep(0.5)
    client = HTBClient(email="user@example.com", password="password", api_base=f"http://localhost:{port}/api/v4/")
    return client
