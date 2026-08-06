# ID: TC-PROJ-002
## test_get_projects_returns_only_user_projects

---

## Objective: 

Validates that the GET request to /projects/ only returns projects listed under
the authenticated user

---

## Preconditions

- API server is running
- Valid user account exists
- Valid authentication is available
- Database is available
- Authenticated user has at least one existing project

---

## Testing Steps

1. Authenticate as a valid user. 
2. Create a new project named "Project A". 
3. Send a GET request to /projects/ using the same user's authentication credentials. 
4. Review that the response status code is 200 OK. 
5. Review the list of projects returned.

---

## Expected Results

 - Request code 200 OK
 - Response contains only one project
 - Returned project is named "Project A"
 - Only projects belonging to the authenticated user are included
in the response

---

## Actual Results
TBD

---

## Testing Type

- Functional
- Integral
- E2E
- Positive test
- Smoke
