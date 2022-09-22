import os
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import uvicorn

from clients.rsvp import RSVPClient
from domain.rsvp import RSVP
from utils import file_utils, security


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


@app.get("/rsvps",
         include_in_schema=False, 
         dependencies=[Depends(security.api_key_auth)])
def get_rsvps() -> List[RSVP]:
    """Return a list of all submitted RSVPs."""
    rsvp_client = RSVPClient()

    try:
        rsvps = rsvp_client.get_rsvps()
    except Exception as e:
        print(e)  # TODO: better logging?
        raise HTTPException(status_code=500, detail="Error retrieving RSVPs")

    return rsvps


@app.get("/rsvps_csv",
         include_in_schema=False,)
def get_rsvps_csv(api_key: str):
    """Return a formatted CSV of all submitted RSVPs."""
    security.api_key_auth(api_key)

    rsvp_client = RSVPClient()
    try:
        rsvps = rsvp_client.get_rsvps()
    except Exception as e:
        print(e)  # TODO: better logging?
        raise HTTPException(status_code=500, detail="Error retrieving RSVPs")

    # return CSV
    export_media_type = 'text/csv'
    export_headers = {
          "Content-Disposition": "attachment; filename=guest_list.csv"
    }
    return StreamingResponse(
        iter([file_utils.rsvps_to_csv(rsvps).getvalue()]),
        headers=export_headers,
        media_type=export_media_type)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")