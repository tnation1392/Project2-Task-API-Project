# ID: TC-USER-006
## test_user_lifecycle

---

## Objective: 

Tests that a user can be created and retrieved from the user
list, then deleted and is no longer accessible after deletion

---

## Preconditions

- API server is running
- Database is available
- Test user doesn't exist yet
- Authentication works correctly

---

## Testing Steps

1. Create a new user called "Lifecycle User"
2. Generate auth headers for the user
3. Send a GET request to /users/.
4. Verify that the response code is 200
5. Verify the user is returned in the users list
6. Send a DELETE request to /users/{id}
7. Verify the response code is 204 No Content
8. Send a GET request to /users/{id} for the deleted user
9. Verify the response code is 401 Unauthorized

---

## Expected Results

- User is created
- User appears in the user list
- Delete operation succeeds
- Deleted user cannot be accessed
- API returns a 401 Unauthorized when trying to retrieve
the deleted user

---

## Actual Results
TBD

---

## Testing Type

- Functional
- Integral
- E2E
- Positive test
- Regression
