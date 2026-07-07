from fastapi import FastAPI
from app.routes.users import router as users_router
from app.routes.projects import router as projects_router
from app.routes.tasks import router as tasks_router
from app.db import Base, engine

app = FastAPI()

app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Task API is running"}
