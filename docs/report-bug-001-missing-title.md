# BUG-001

## Summary
POST /tasks returns 500 error when title field is missing.

## Priority
High

## Severity
Major

## Environment
- Windows 11
- Python 3.13

---

## Steps to Reproduce

1. Send POST request to /tasks
2. Omit title field
3. Submit request

---

## Expected Result

API returns HTTP 400 with validation error.

---

## Actual Result

API returns HTTP 500.

---

## Status

Open