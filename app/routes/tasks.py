from fastapi import APIRouter, Depends, HTTPException
from app.models import tasks_db, projects_db
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.auth import get_current_user
from app.rules import validate_task_transition
import uuid

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/projects/{project_id}", response_model=TaskResponse)
def create_task(
    project_id: str,
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
):
    project = projects_db.get(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    task_id = str(uuid.uuid4())

    new_task = {
        "id": task_id,
        "title": task.title,
        "status": "todo",
        "project_id": project_id,
    }

    tasks_db[task_id] = new_task

    return new_task


@router.get("/projects/{project_id}")
def get_tasks(project_id: str, current_user: dict = Depends(get_current_user)):
    project = projects_db.get(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return [
        task
        for task in tasks_db.values()
        if task["project_id"] == project_id
    ]


@router.patch("/{task_id}")
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
):
    task = tasks_db.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = projects_db.get(task["project_id"])

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    validate_task_transition(task["status"], task_update.status)

    task["status"] = task_update.status

    return task


@router.delete("/{task_id}")
def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    task = tasks_db.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = projects_db.get(task["project_id"])

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    del tasks_db[task_id]

    return {"message": "Task deleted"}
