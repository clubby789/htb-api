from hackthebox import HTBClient
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env')
load_dotenv(os.path.abspath(env_path))
client = HTBClient(email=os.getenv("HTB_EMAIL"), password=os.getenv("HTB_PASSWORD"))
