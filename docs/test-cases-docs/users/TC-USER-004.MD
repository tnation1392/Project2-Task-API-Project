# ID: TC-USER-004
## test_get_users_requires_auth

---

## Objective

Verifies that the /users/ endpoint requires authentication

---

## Preconditions

- API server is running
- Database is available
- No authentication header is present in the request

---

## Testing Steps

1. Send a GET request to /users/
2. Do not include an API Key or auth header in the request
3. Submit the request
4. Review that the response code is 401 Unauthorized

---

## Expected Results

- Response code is 401 Unauthorized

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