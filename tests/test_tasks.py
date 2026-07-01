import pytest
import asyncio
from datetime import datetime
from tests.helpers import create_user, build_auth_headers, create_project, create_task


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_create_task(client, auth_headers):
    project_res = await client.post(
        "/projects/", json={"name": "Task Project"}, headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Test Task"},
        headers=auth_headers,
    )

    assert task_res.status_code == 201


@pytest.mark.asyncio
async def test_get_tasks_for_project(client, auth_headers):
    project_res = await client.post(
        "/projects/", json={"name": "Task Project"}, headers=auth_headers
    )
    project_id = project_res.json()["id"]

    await client.post(
        f"/tasks/projects/{project_id}", json={"title": "Task 1"}, headers=auth_headers
    )

    res = await client.get(f"/tasks/projects/{project_id}", headers=auth_headers)

    assert res.status_code == 200
    tasks = res.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"


@pytest.mark.asyncio
async def test_cannot_create_task_in_other_users_project(client):
    res_a = await client.post("/users/", json={"name": "User A"})
    user_a = res_a.json()
    headers_a = {"x-api-key": user_a["api_key"]}

    project_res = await client.post(
        "/projects/", json={"name": "Private"}, headers=headers_a
    )
    project_id = project_res.json()["id"]

    res_b = await client.post("/users/", json={"name": "User B"})
    user_b = res_b.json()
    headers_b = {"x-api-key": user_b["api_key"]}

    res = await client.post(
        f"/tasks/projects/{project_id}", json={"title": "Hack Task"}, headers=headers_b
    )

    assert res.status_code == 403


@pytest.mark.asyncio
async def test_create_task_missing_title(client, auth_headers):
    project_res = await client.post(
        "/projects/", json={"name": "Task Project"}, headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": ""},
        headers=auth_headers,
    )

    assert task_res.status_code == 422


@pytest.mark.asyncio
async def test_create_task_invalid_project(client, auth_headers):
    res = await client.post(
        "/tasks/projects/invalid-id", json={"title": "Test Task"}, headers=auth_headers
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_update_task_status(client):
    user = await create_user(client, name="Task Owner")
    headers = build_auth_headers(user)

    project = await create_project(client, headers, name="Update Project")
    task = await create_task(client, headers, project["id"], title="Task")

    first_update = await client.patch(
        f"/tasks/{task['id']}", json={"status": "in_progress"}, headers=headers
    )
    assert first_update.status_code == 200

    second_update = await client.patch(
        f"/tasks/{task['id']}", json={"status": "done"}, headers=headers
    )
    assert second_update.status_code == 200


@pytest.mark.asyncio
async def test_update_task_invalid_status(client, auth_headers):
    project_res = await client.post(
        "/projects/", json={"name": "Validation"}, headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}", json={"title": "Task"}, headers=auth_headers
    )
    task_id = task_res.json()["id"]

    res = await client.patch(
        f"/tasks/{task_id}", json={"status": "invalid"}, headers=auth_headers
    )

    assert res.status_code == 422


@pytest.mark.asyncio
async def test_delete_task(client, auth_headers):
    project_res = await client.post(
        "/projects/", json={"name": "Delete Task"}, headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}", json={"title": "Task"}, headers=auth_headers
    )
    task_id = task_res.json()["id"]

    delete_res = await client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert delete_res.status_code == 204

    get_res = await client.patch(
        f"/tasks/{task_id}", json={"status": "done"}, headers=auth_headers
    )
    assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_update_task_valid_transition_to_in_progress(client):
    user = await create_user(client, name="Task Owner")
    headers = build_auth_headers(user)

    project = await create_project(client, headers, name="Workflow Project")
    task = await create_task(client, headers, project["id"], title="Workflow Task")

    update_res = await client.patch(
        f"/tasks/{task['id']}", json={"status": "in_progress"}, headers=headers
    )

    assert update_res.status_code == 200


@pytest.mark.asyncio
async def test_update_task_invalid_transition_todo_to_done(client, auth_headers):
    project_res = await client.post(
        "/projects/", json={"name": "Workflow Project"}, headers=auth_headers
    )
    project_id = project_res.json()["id"]

    task_res = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Workflow Task"},
        headers=auth_headers,
    )
    task_id = task_res.json()["id"]

    update_res = await client.patch(
        f"/tasks/{task_id}", json={"status": "done"}, headers=auth_headers
    )

    assert update_res.status_code == 409


@pytest.mark.asyncio
async def test_create_task_whitespace_only_title(client, auth_headers):
    project_res = await client.post(
        "/projects/", json={"name": "Validation Project"}, headers=auth_headers
    )
    project_id = project_res.json()["id"]

    response = await client.post(
        f"/tasks/projects/{project_id}", json={"title": "   "}, headers=auth_headers
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_cannot_create_duplicate_task_title_in_same_project(client, auth_headers):
    project_res = await client.post(
        "/projects/", json={"name": "Task Validation Project"}, headers=auth_headers
    )
    project_id = project_res.json()["id"]

    first_response = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Duplicate Task"},
        headers=auth_headers,
    )
    assert first_response.status_code == 201

    second_response = await client.post(
        f"/tasks/projects/{project_id}",
        json={"title": "Duplicate Task"},
        headers=auth_headers,
    )

    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_create_task_includes_timestamps(client):
    user = await create_user(client, name="Timestamp User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Timestamp Project")

    response = await client.post(
        f"/tasks/projects/{project['id']}",
        json={"title": "Timestamp Task"},
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()

    assert "created_at" in data
    assert "updated_at" in data

    created_at = datetime.fromisoformat(data["created_at"])
    updated_at = datetime.fromisoformat(data["updated_at"])

    assert created_at <= updated_at


@pytest.mark.asyncio
async def test_get_tasks_filter_by_status(client):
    user = await create_user(client, name="Filter User")
    headers = build_auth_headers(user)
    project = await create_project(client, headers, name="Filter Project")

    task1 = await create_task(client, headers, project["id"], title="Task One")
    task2 = await create_task(client, headers, project["id"], title="Task Two")

    await client.patch(
        f"/tasks/{task2['id']}", json={"status": "in_progress"}, headers=headers
    )

    response = await client.get(
        f"/tasks/projects/{project['id']}?status=in_progress", headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "in_progress"
