import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")


def api_key_is_valid(api_key: str):
    prod_api_key = os.getenv('API_KEY')
    if api_key != prod_api_key:
        return False
    return True


def api_key_auth(api_key: str = Depends(OAUTH2_SCHEME)):
    """Handle API key for restricted endpoints"""
    if not api_key_is_valid(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Scram, you damn turkey."
        )
