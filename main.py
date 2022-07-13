from fastapi import FastAPI, HTTPException

from clients.rsvp import RSVPClient
from domain.rsvp import RSVP


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/rsvp")
def submit_rsvp(rsvp: RSVP):
    rsvp_client = RSVPClient()
    
    try:
        rsvp_client.submit_rsvp(rsvp)
    except Exception as e:
        print(e)  # TODO: better logging?
        raise HTTPException(status_code=500, detail="Error submitting RSVP")
    
    return {'success': True}
