# ID: TC-USER-003
## test_create_user_invalid_inputs

---

## Objective: 

Tests that a user cannot be created with multiple incorrect
inputs.

Uses parametrization to test the inputs:
- {"To"}
- {""}
- {"a" * 100}

---

## Preconditions

- API server is running
- Database is available

---

## Testing Steps

1. Send a POST request to /users/
2. Include the payloads:
- {"name": "To"}
- {"name": ""}
- {"name": "a" * 100}
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