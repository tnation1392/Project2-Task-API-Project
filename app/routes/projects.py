from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.db_models import Project
from app.schemas import ProjectCreate, ProjectResponse
from app.auth import get_current_user, is_admin
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_or_404(db: Session, project_id: str):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return project


def get_authorized_project(db: Session, project_id: str, current_user: dict):
    project = get_project_or_404(db, project_id)

    if not is_admin(current_user) and project.owner_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    return project


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_project = (
        db.query(Project)
        .filter(
            Project.owner_id == current_user["id"],
            Project.name.ilike(project.name.strip()),
        )
        .first()
    )

    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project name already exists for this user",
        )

    new_project = Project(
        id=str(uuid.uuid4()),
        name=project.name.strip(),
        owner_id=current_user["id"],
    )

    try:
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project",
        )

    return new_project


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if is_admin(current_user):
        projects = db.query(Project).all()
    else:
        projects = (
            db.query(Project).filter(Project.owner_id == current_user["id"]).all()
        )

    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = get_authorized_project(db, project_id, current_user)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = get_authorized_project(db, project_id, current_user)

    try:
        db.delete(project)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project",
        )

    return
