import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

URI = os.getenv("MONGO_URI")

client = MongoClient(URI, tlsInsecure=True)

def get_db():
    return client["health_ally"]["data"]

get_db().delete_many({})