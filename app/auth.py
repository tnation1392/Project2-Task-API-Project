import uuid
from fastapi import Header, HTTPException
from app.models import users_db


def get_current_user(x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    # Find user by API key
    for user in users_db.values():
        if user["api_key"] == x_api_key:
            return user

    raise HTTPException(status_code=401, detail="Invalid API key")


def generate_api_key():
    return str(uuid.uuid4())
