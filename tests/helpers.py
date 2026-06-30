#A helper to create a user via POST /users/ and return a JSON response
async def create_user(client, name="Test User", role="member"):
    response = await client.post("/users/", json={"name": name, "role": role})
    assert response.status_code == 200
    return response.json()


#A helper to build an X-API-Key header dict from user response
def build_auth_headers(user_data):
    return {"x-api-key": user_data["api_key"]}

#A helper to create a project via POST /projects/ and return a JSON response
async def create_project(client, headers, name="Test Project"):
    response = await client.post("/projects/", json={"name": name}, headers=headers)
    assert response.status_code == 200
    return response.json()

#A helper to create a task via POST /tasks/projects{id} and return a JSON response
async def create_task(client, headers, project_id, title="Test Task"):
    response = await client.post(
        f"/tasks/projects/{project_id}", json={"title": title}, headers=headers
    )
    assert response.status_code == 200
    return response.json()
