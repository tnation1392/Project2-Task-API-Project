# ID: TC-USER-002
## test_create_user_invalid_name

---

## Objective: 

Tests that a user cannot be created with an invalid name
that is too short (2 characters)

---

## Preconditions

- API server is running
- Database is available

---

## Testing Steps

1. Send a POST request to /users/
2. Include the payload:
{
  "name": "To"
}
3. Submit request
4. Verify that the response code is 422 Unprocessable

---

## Expected Results

- Response code is 422 Unprocessable

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