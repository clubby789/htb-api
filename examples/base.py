import os
import sys
from dotenv import load_dotenv

parent = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
env_path = os.path.join(parent, ".env")
load_dotenv(os.path.abspath(env_path))
sys.path.append(parent)
from hackthebox import HTBClient

client = HTBClient(email=os.getenv("HTB_EMAIL"), password=os.getenv("HTB_PASSWORD"))
