import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


USERNAME = os.getenv('MONGO_USERNAME')
PASSWORD = os.getenv('MONGO_PASSWORD')


class AbstractDatabaseClient:
    """Facilitates communication with a DB"""
    def insert_rsvp(self, rsvp):
        raise NotImplementedError
    
    def get_rsvps(self):
        raise NotImplementedError

class MongoDBClient(AbstractDatabaseClient):
    """Facilitates communication with cloud-based MongoDB database"""
    def __init__(self):
        self.client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.r3aqr.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.main

    def insert_rsvp(self, rsvp):
        collection = self.db['rsvp']
        collection.insert_one(rsvp.to_dict())

    def get_rsvps(self):
        collection = self.db['rsvp']

        from domain.rsvp import RSVP
        clean_rsvps = [
            RSVP(
                party_name=raw['party_name'],
                message=raw['message'],
                attending=raw['attending'],
                people=raw['people'],
                rsvp_time=raw['rsvp_time']
            ) for raw in collection.find()]

        return clean_rsvps
