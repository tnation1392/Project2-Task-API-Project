from fastapi import APIRouter, HTTPException, Depends
from app.models import users_db
from app.schemas import UserCreate, UserResponse
from app.auth import generate_api_key, get_current_user
import uuid

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    user_id = str(uuid.uuid4())
    api_key = generate_api_key()

    new_user = {
        "id": user_id,
        "name": user.name,
        "api_key": api_key
    }

    users_db[user_id] = new_user

    return new_user

@router.get("/")
def get_users(current_user: dict = Depends(get_current_user)):
    return list(users_db.values())

@router.get("/{user_id}")
def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    user = users_db.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.delete("/{user_id}")
def delete_user(user_id: str, current_user: dict = Depends(get_current_user)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    del users_db[user_id]

    return {"message": "User deleted"}


