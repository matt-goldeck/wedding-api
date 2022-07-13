from domain.rsvp import RSVP, RSVPRepository


class RSVPClient:
    def submit_rsvp(self, rsvp: RSVP):
        repository = RSVPRepository()
        repository.insert_rsvp(rsvp)
