# ID: TC-USER-008
## test_missing_api_key

---

## Objective: 

Verifies that the GET request for /users/ with an missing API Key will draw 
a response code of 401 Unauthorized

---

## Preconditions

- API server is running
- Database is available

---

## Testing Steps

1. Send a GET request to /users/
2. Do not include an API key in the request
3. Submit the request
4. Review that the response code is 401 Unauthorized

---

## Expected Results

 - Request code 401 Unauthorized

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
