# ID: TC-USER-005
## test_get_users_success

---

## Objective

Verifies that GET request with the /users/ endpoint with authentication successfully
returns a list of users

---

## Preconditions

- API server is running
- Database is available
- Authentication header/API Key is present in the request

---

## Testing Steps

1. Send a GET request to /users/
2. Include an API Key or auth header in the request
3. Submit the request
4. Review that the response code is 200 Success

---

## Expected Results

- Response code is 200 Success

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