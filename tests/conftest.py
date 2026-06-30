import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import SessionLocal
from app.db_models import User, Project, Task

#A fixture to clear the database before each test for purity of environment
@pytest.fixture(autouse=True)
def clear_databases():
    db = SessionLocal()
    try:
        db.query(Task).delete()
        db.query(Project).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()

#A fixture to make an HTTP client to test the FastAPI app
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

#A fixture to create and return a test use with an api_key
@pytest.fixture
async def auth_user(client):
    response = await client.post("/users/", json={"name": "Test User"})
    data = response.json()

    return {"user_id": data["id"], "api_key": data["api_key"]}

#A fixture to build an X-API-key header dictionary from the auth_user fixture
@pytest.fixture
async def auth_headers(auth_user):
    return {"x-api-key": auth_user["api_key"]}
