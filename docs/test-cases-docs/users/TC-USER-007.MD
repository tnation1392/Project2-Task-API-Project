# ID: TC-USER-007
## test_invalid_api_key

---

## Objective: 

Tests that the GET request for /users/ with an invalid API Key will draw 
a response code of 401 Unauthorized

---

## Preconditions

- API server is running
- Database is available

---

## Testing Steps

1. Send a GET request to /users/
2. Include an invalid API Key {"x-api-key: "fake_key"}
3. Submit the request
4. Review that the response code is 401 Unauthorized

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
- Negative test
- Smoke
