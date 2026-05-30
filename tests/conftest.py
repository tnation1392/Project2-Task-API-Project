import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models import users_db, projects_db, tasks_db


@pytest.fixture(autouse=True)
def clear_databases():
    users_db.clear()
    projects_db.clear()
    tasks_db.clear()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_user(client):
    response = await client.post("/users/", json={"name": "Test User"})
    data = response.json()

    return {
        "user_id": data["id"],
        "api_key": data["api_key"]
    }


@pytest.fixture
async def auth_headers(auth_user):
    return {"x-api-key": auth_user["api_key"]}