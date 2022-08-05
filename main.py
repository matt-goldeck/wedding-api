import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from clients.rsvp import RSVPClient
from domain.rsvp import RSVP

app = FastAPI()

# = Handle CORS crap =
origins = ["*"]  # lol what could go wrong
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# = Routes =

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")