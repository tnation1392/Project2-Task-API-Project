# ID: TC-USER-001
## test_create_user

---

## Objective: 

Tests that a user can be created and retrieved via JSON

---

## Preconditions

- API server is running
- Database is available
- Test user doesn't exist yet

---

## Testing Steps

1. Send a POST request to /users/
2. Include the payload:
{
  "name": "Todd"
}
3. Submit request
4. Review the response body and see that the response
code is 201 Created

---

## Expected Results

- User is created
- Response code is 201 Created
- Response contains "Todd"
- Response contains an api_key field
- Both id and api_key are returned as strings

---

## Actual Results
TBD

---

## Testing Type

- Functional
- Integral
- E2E
