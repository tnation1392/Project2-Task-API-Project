import pytest


@pytest.mark.asyncio
async def test_create_task(client, auth_headers):
    # Create project first
    project_res = await client.post(
        "/projects/",
        json={"name": "Task Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    # Create task
    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Test Task"},
        headers=auth_headers
    )

    assert task_res.status_code == 200

    data = task_res.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "todo"
    assert data["project_id"] == project_id

@pytest.mark.asyncio
async def test_get_tasks_for_project(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Task Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Task 1"},
        headers=auth_headers
    )

    res = await client.get(f"/tasks/projects/{project_id}", headers=auth_headers)

    assert res.status_code == 200
    tasks = res.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"

@pytest.mark.asyncio
async def test_cannot_create_task_in_other_users_project(client):
    # User A
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    # Create project with User A
    project_res = await client.post(
        "/projects/",
        json={"name": "Private"},
        headers=headers_a
    )
    project_id = project_res.json()["id"]

    # User B
    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    # User B tries to create task
    res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Hack Task"},
        headers=headers_b
    )

    assert res.status_code == 403

@pytest.mark.asyncio
async def test_create_task_invalid_project(client, auth_headers):
    res = await client.post(
        "/tasks/projects/invalid-id",
        json={"title": "Test Task"},
        headers=auth_headers
    )

    assert res.status_code == 404

@pytest.mark.asyncio
async def test_update_task_status(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Update Project"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Task"},
        headers=auth_headers
    )
    task_id = task_res.json()["id"]

    update_res = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["status"] == "done"

@pytest.mark.asyncio
async def test_update_task_invalid_status(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Validation"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Task"},
        headers=auth_headers
    )
    task_id = task_res.json()["id"]

    res = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "invalid"},
        headers=auth_headers
    )

    assert res.status_code == 422

@pytest.mark.asyncio
async def test_delete_task(client, auth_headers):
    project_res = await client.post(
        "/projects/",
        json={"name": "Delete Task"},
        headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Task"},
        headers=auth_headers
    )
    task_id = task_res.json()["id"]

    delete_res = await client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert delete_res.status_code == 200

    # verify gone
    get_res = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers
    )
    assert get_res.status_code == 404
