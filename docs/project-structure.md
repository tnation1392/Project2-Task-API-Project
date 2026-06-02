# Project Structure

This document explains how the `task-api-project` repository is organized and how the main application, automation, and documentation pieces fit together.

---

## Repository Layout

```text
task-api-project/
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI pipeline
│
├── app/                            # FastAPI application code
│   ├── routes/                     # API route definitions
│   │   ├── projects.py             # Project endpoints
│   │   ├── tasks.py                # Task endpoints
│   │   └── users.py                # User endpoints
│   ├── __init__.py                 # Marks app as a Python package
│   ├── auth.py                     # Authentication / authorization helpers
│   ├── db.py                       # Database configuration / session setup
│   ├── db_models.py                # SQLAlchemy ORM models
│   ├── main.py                     # FastAPI app entry point
│   ├── models.py                   # Application/domain models
│   ├── rules.py                    # Business rules / workflow validation
│   └── schemas.py                  # Request / response schemas
│
├── docs/                           # Supporting documentation
│   ├── testing-strategy.md         # QA / testing strategy
│   └── project-structure.md        # Repository structure guide
│
├── tests/                          # Automated QA test suite
│   ├── conftest.py                 # Shared pytest fixtures
│   ├── helpers.py                  # Test helpers / reusable setup utilities
│   ├── test_openapi_contract.py    # OpenAPI contract validation tests
│   ├── test_projects.py            # Projects API tests
│   ├── test_tasks.py               # Tasks API tests
│   └── test_users.py               # Users API tests
│
├── .dockerignore                   # Docker build exclusions
├── docker-compose.yaml             # Docker Compose configuration
├── Dockerfile                      # Container build definition
├── pyproject.toml                  # Project/tooling configuration
├── pytest.ini                      # Pytest configuration
├── README.md                       # Main project overview
├── report.html                     # Generated HTML test report
├── requirements.txt                # Python dependencies
└── task_api.db                     # Local SQLite database file