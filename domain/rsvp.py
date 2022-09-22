from dataclasses import dataclass
from typing import Optional, List

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

    def to_csv_dict(self):
        """to a dict, but pretty"""
        return {
            'Party Name': self.party_name,
            'Attendance': self.attending,
            'Number Attending': len(self.people) if self.attending else 0,
            'People': self.people,
            'Message': self.message,
            'RSVP Submitted At': self.rsvp_time,
        }


class RSVPRepository:
    def __init__(self, db_client=MongoDBClient()):
        self.db_client = db_client

    def insert_rsvp(self, rsvp: RSVP):
        self.db_client.insert_rsvp(rsvp)

    def get_rsvps(self) -> List[RSVP]:
        return self.db_client.get_rsvps()