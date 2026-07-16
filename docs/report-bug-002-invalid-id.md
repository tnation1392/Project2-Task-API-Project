# BUG-002

## Summary
The API returns an incorrect HTTP Status Code when a request
is made with a non-existent task ID

## Priority
High

## Severity
Major

## Environment
- Windows 11
- Python 3.13

---
## Preconditions
- Application is running
- Task ID '9999' does not exist

## Steps to Reproduce

1. Send GET request to:
```http GET /tasks/9999```
2. Observe response

---

## Expected Result

API returns HTTP 404 Not Found

---

## Actual Result

API returns HTTP 200 OK

---

## Status

Open