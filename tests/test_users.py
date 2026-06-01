import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/users/", json={"name": "Todd"})

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["id"], str)
    assert data["name"] == "Todd"
    assert isinstance(data["api_key"], str)

@pytest.mark.asyncio
async def test_create_user_invalid_name(client):
    response = await client.post("/users/", json={"name": "To"})

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_name", [
    "To",          # too short
    "",            # empty
    "a" * 100      # too long
])
async def test_create_user_invalid_inputs(client, invalid_name):
    response = await client.post("/users/", json={"name": invalid_name})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_users_requires_auth(client):
    response = await client.get("/users/")

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_users_success(client, auth_headers):
    response = await client.get("/users/", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_user_lifecycle(client):
    # Create user
    create_res = await client.post("/users/", json={"name": "Lifecycle User"})
    assert create_res.status_code == 200
    user = create_res.json()

    headers = {"x-api-key": user["api_key"]}

    # Get users
    get_res = await client.get("/users/", headers=headers)
    assert get_res.status_code == 200

    users = get_res.json()
    assert any(u["id"] == user["id"] for u in users)

    # Delete user
    delete_res = await client.delete(f"/users/{user['id']}", headers=headers)
    assert delete_res.status_code == 200

    # Verify deleted
    get_res = await client.get(f"/users/{user['id']}", headers=headers)
    assert get_res.status_code == 401

@pytest.mark.asyncio
async def test_invalid_api_key(client):
    headers = {"x-api-key": "fake_key"}

    response = await client.get("/users/", headers=headers)

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_missing_api_key(client):
    response = await client.get("/users/")

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_user_whitespace_only_name(client):
    response = await client.post("/users/", json={"name": "   "})

    assert response.status_code == 422
