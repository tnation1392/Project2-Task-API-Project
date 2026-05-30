import pytest


@pytest.mark.asyncio
async def test_create_project(client, auth_headers):
    response = await client.post(
        "/projects/",
        json={"name": "Test Project"},
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Project"
    assert "id" in data
    assert "owner_id" in data

@pytest.mark.asyncio
async def test_get_projects_returns_only_user_projects(client, auth_user, auth_headers):
    # Create project for this user
    await client.post("/projects/", json={"name": "Project A"}, headers=auth_headers)

    response = await client.get("/projects/", headers=auth_headers)

    assert response.status_code == 200

    projects = response.json()
    assert len(projects) == 1
    assert projects[0]["name"] == "Project A"

@pytest.mark.asyncio
async def test_users_cannot_see_each_others_projects(client):
    # User A
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    # User B
    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    # User A creates project
    await client.post("/projects/", json={"name": "A Project"}, headers=headers_a)

    # User B fetches projects
    res = await client.get("/projects/", headers=headers_b)

    assert res.status_code == 200
    assert res.json() == []  # Should NOT see User A's project

@pytest.mark.asyncio
async def test_cannot_access_other_users_project(client):
    # Create User A
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    # Create project with User A
    project_res = await client.post(
        "/projects/",
        json={"name": "Private Project"},
        headers=headers_a
    )
    project_id = project_res.json()["id"]

    # Create User B
    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    # User B tries to access User A's project
    res = await client.get(f"/projects/{project_id}", headers=headers_b)

    assert res.status_code == 403

@pytest.mark.asyncio
async def test_get_nonexistent_project(client, auth_headers):
    res = await client.get("/projects/nonexistent-id", headers=auth_headers)

    assert res.status_code == 404

@pytest.mark.asyncio
async def test_delete_project(client, auth_headers):
    # Create project
    res = await client.post("/projects/", json={"name": "Delete Me"}, headers=auth_headers)
    project_id = res.json()["id"]

    # Delete it
    delete_res = await client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert delete_res.status_code == 200

    # Verify it's gone
    get_res = await client.get(f"/projects/{project_id}", headers=auth_headers)
    assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_projects_require_auth(client):
    res = await client.get("/projects/")

    assert res.status_code == 401
