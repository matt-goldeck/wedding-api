from dataclasses import dataclass
from typing import Optional

from clients.database import MongoDBClient


@dataclass
class Person:
    first_name: str
    last_name: str


@dataclass
class RSVP:
    party_id: str
    attending: bool
    people: Optional[list[Person]]

    def to_dict(self):
        return {
            'party_id': self.party_id,
            'attending': self.attending,
            'people': [p.__dict__ for p in self.people]
        }


class RSVPRepository:
    def __init__(self, db_client=MongoDBClient()):
        self.db_client = db_client

    def insert_rsvp(self, rsvp: RSVP):
        self.db_client.insert_rsvp(rsvp)
