# ID: TC-USER-009
## test_create_user_whitespace_only_name

---

## Objective: 

Tests that the POST request for /users/ with a whitespace only name will
return a request code 422 Unprocessable

---

## Preconditions

- API server is running
- Database is available

---

## Testing Steps

1. Send a POST request to /users/
2. Enter whitespace as the username
3. Submit the request
4. Review that the response code is 422 Unprocessable

---

## Expected Results

 - Request code 422 Unprocessable

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
