from fastapi import FastAPI
from app.routes import users, projects, tasks
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "Task API is running"}
