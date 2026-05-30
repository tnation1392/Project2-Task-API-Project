from fastapi import APIRouter, Depends, HTTPException
from app.models import projects_db
from app.schemas import ProjectCreate, ProjectResponse
from app.auth import get_current_user
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    current_user: dict = Depends(get_current_user),
):
    project_id = str(uuid.uuid4())

    new_project = {
        "id": project_id,
        "name": project.name,
        "owner_id": current_user["id"],
    }

    projects_db[project_id] = new_project

    return new_project

@router.get("/{project_id}")
def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    project = projects_db.get(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return project

@router.get("/")
def get_projects(current_user: dict = Depends(get_current_user)):
    return [
        project
        for project in projects_db.values()
        if project["owner_id"] == current_user["id"]
    ]

@router.delete("/{project_id}")
def delete_project(project_id: str, current_user: dict = Depends(get_current_user)):
    project = projects_db.get(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    del projects_db[project_id]

    return {"message": "Project deleted"}