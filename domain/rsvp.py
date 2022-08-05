from dataclasses import dataclass
from typing import Optional

from clients.database import MongoDBClient


@dataclass
class RSVP:
    party_name: str
    message: str
    attending: bool
    people: Optional[list]
    rsvp_time: str

    def to_dict(self):
        return {
            'party_name': self.party_name,
            'message': self.message,
            'attending': self.attending,
            'people': self.people,
            'rsvp_time': self.rsvp_time
        }


class RSVPRepository:
    def __init__(self, db_client=MongoDBClient()):
        self.db_client = db_client

    def insert_rsvp(self, rsvp: RSVP):
        self.db_client.insert_rsvp(rsvp)
