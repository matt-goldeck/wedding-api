import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


USERNAME = os.getenv('MONGO_USERNAME')
PASSWORD = os.getenv('MONGO_PASSWORD')


class AbstractDatabaseClient:
    """Facilitates communication with a DB"""
    def insert_rsvp(self, rsvp):
        pass


class MongoDBClient(AbstractDatabaseClient):
    """Facilitates communication with cloud-based MongoDB database"""
    def __init__(self):
        self.client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.r3aqr.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.main

    def insert_rsvp(self, rsvp):
        collection = self.db['rsvp']
        collection.insert_one(rsvp.to_dict())
