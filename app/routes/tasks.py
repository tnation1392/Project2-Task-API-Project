from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.db_models import Task, Project
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.auth import get_current_user, is_admin
from app.rules import validate_task_transition
import uuid

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_authorized_project(db: Session, project_id: str, current_user: dict):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    if not is_admin(current_user) and project.owner_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    return project


def get_task_or_404(db: Session, task_id: str):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


@router.post(
    "/projects/{project_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    project_id: str,
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = get_authorized_project(db, project_id, current_user)

    # Prevent duplicate titles (case-insensitive)
    existing_task = (
        db.query(Task)
        .filter(Task.project_id == project_id, Task.title.ilike(task.title.strip()))
        .first()
    )

    if existing_task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task title already exists in this project",
        )

    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title.strip(),
        status="todo",
        project_id=project_id,
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        )

    return new_task


@router.get("/projects/{project_id}", response_model=list[TaskResponse])
@router.get("/projects/{project_id}", response_model=list[TaskResponse])
def get_tasks(
    project_id: str,
    status: str | None = Query(None),
    title: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_authorized_project(db, project_id, current_user)

    query = db.query(Task).filter(Task.project_id == project_id)

    if status:
        query = query.filter(Task.status == status)

    if title:
        query = query.filter(Task.title.ilike(f"%{title}%"))

    offset = (page - 1) * size
    tasks = query.offset(offset).limit(size).all()

    return tasks


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = get_task_or_404(db, task_id)
    project = get_authorized_project(db, task.project_id, current_user)

    # Handle partial updates safely
    if task_update.status is not None:
        validate_task_transition(task.status, task_update.status)
        task.status = task_update.status

    try:
        db.commit()
        db.refresh(task)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task",
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = get_task_or_404(db, task_id)
    get_authorized_project(db, task.project_id, current_user)

    try:
        db.delete(task)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task",
        )

    return


def validate_task_transition(current, new):
    valid = {"todo": ["in_progress"], "in_progress": ["done"], "done": []}

    if new not in valid.get(current, []):
        raise HTTPException(status_code=409, detail="Invalid status transition")
