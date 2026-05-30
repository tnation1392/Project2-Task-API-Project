from pydantic import BaseModel, Field
from typing import Literal

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

class UserResponse(BaseModel):
    id: str
    name: str
    api_key: str

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)

class ProjectResponse(BaseModel):
    id: str
    name: str
    owner_id: str

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)

class TaskResponse(BaseModel):
    id: str
    title: str
    status: str
    project_id: str

class TaskUpdate(BaseModel):
    status: Literal["todo", "in_progress", "done"]