# Task API Project

A FastAPI task management API built as a QA automation portfolio project.

The goal of this project was to learn API development and automated testing while practicing the kinds of scenarios commonly tested by QA Automation Engineers. During development, the project evolved from using in-memory storage to a database-backed application using SQLite and SQLAlchemy.

The project includes API authentication, authorization, validation, filtering, pagination, workflow rules, automated testing, OpenAPI contract checks, and GitHub Actions CI.

---

# Project Overview

This project started as a simple FastAPI application and was gradually expanded to include more realistic backend functionality.

As development continued, the project was upgraded to include:

- SQLite database persistence
- SQLAlchemy ORM models
- User, Project, and Task relationships
- Authentication and authorization
- Workflow validation rules
- Filtering and pagination
- OpenAPI contract testing
- CI/CD automation with GitHub Actions

The project was also used to practice API test automation with pytest and httpx.

---

# What I Learned

This project gave me hands-on experience with:

- Building REST APIs using FastAPI
- Creating database models using SQLAlchemy
- Working with SQLite databases
- Using dependency injection for database sessions
- Writing automated API tests with pytest
- Testing authentication and authorization behavior
- Creating positive, negative, and edge-case tests
- Validating OpenAPI contracts
- Configuring CI pipelines with GitHub Actions
- Debugging integration issues between application code, database models, and tests

---

# Database Upgrade

One of the biggest milestones in this project was migrating from in-memory storage to a SQLite database.

## Before the Migration

- Data was stored in Python data structures
- Data was lost when the application restarted
- Resource relationships were simplified

## After the Migration

- Data is persisted in SQLite
- SQLAlchemy models are used for Users, Projects, and Tasks
- Projects are linked to Users
- Tasks are linked to Projects
- Automated tests validate database-backed behavior

This migration required refactoring API routes, updating automated tests, and troubleshooting several issues related to database persistence, authentication, route registration, status codes, filtering, and API contracts.

---

# API Features

## Resources

- Users
- Projects
- Tasks

## Functionality

- Create, read, update, and delete operations
- SQLite database persistence
- SQLAlchemy ORM integration
- Request validation using Pydantic
- Timestamp tracking
- Filtering support
- Pagination support
- Task workflow validation

## Authentication & Authorization

### Authentication

- API key authentication

### Authorization

- Project ownership validation
- Role-based access control

Roles:

- member
- admin

---

# Testing Focus

This project was built with testing as a major focus.

The automated test suite covers:

- Positive API scenarios
- Negative API scenarios
- Authentication testing
- Authorization testing
- Validation testing
- Task workflow rules
- Filtering behavior
- Pagination behavior
- Database persistence
- OpenAPI contract validation

## Testing Tools Used

- pytest
- pytest-asyncio
- httpx
- pytest-cov
- pytest-html

---

# OpenAPI Contract Testing

The project includes automated tests that validate the generated OpenAPI schema.

Current checks include:

- OpenAPI schema availability
- Published API paths
- Expected HTTP methods
- Security metadata for protected endpoints

These tests help detect accidental API contract changes before they are merged.

---

# Tech Stack

## Backend

- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

## Testing

- pytest
- pytest-asyncio
- httpx
- pytest-cov
- pytest-html

## Quality & CI

- GitHub Actions
- Black
- Flake8

## Language

- Python 3.11+

---

# Project Structure

```text
project2-task-api-project/
├── app/
│   ├── routes/
│   ├── schemas/
│   ├── db.py
│   ├── db_models.py
│   └── main.py
├── docs/
│   ├── testing-strategy.md
│   └── testing-structure.md
├── tests/
├── .github/
│   └── workflows/
├── README.md
├── requirements.txt
└── ...
```

---

# Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/tnation1392/project2-task-api-project.git
cd project2-task-api-project
```

## 2. Create and Activate a Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the API

```bash
uvicorn app.main:app --reload
```

## 5. Open the API Documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI Schema: http://127.0.0.1:8000/openapi.json

---

# Running Tests

## Run All Tests

```bash
pytest -v
```

## Run Smoke Tests

```bash
pytest -m smoke -v
```

## Run Regression Tests

```bash
pytest -m regression -v
```

## Run With Coverage

```bash
pytest --cov=app --cov-report=term-missing
```

## Generate an HTML Test Report

```bash
pytest --html=report.html --self-contained-html
```

---

# CI Quality Gates

The GitHub Actions pipeline is configured to:

- Install dependencies
- Check formatting with Black
- Lint with Flake8
- Run the pytest suite
- Verify code coverage
- Generate HTML test reports

This helps keep the project aligned with real-world QA automation workflows and continuous integration practices.

---

# Database

The application uses SQLite as its persistence layer and SQLAlchemy as its ORM.

## Database Responsibilities

- User storage
- Project ownership tracking
- Task persistence
- Resource relationships
- Timestamp auditing

## Benefits of Adding a Database

- Data persists across application restarts
- More realistic API behavior
- Better validation of user ownership rules
- Improved integration testing
- Ability to test multi-step workflows

Database tables are created automatically when the application starts.

Example database file:

```text
task_api.db
```

---

# Documentation

Additional documentation:

- docs/testing-strategy.md
- docs/testing-structure.md

---

# Completed Features

- SQLite persistence
- SQLAlchemy ORM integration
- User, Project, and Task models
- CRUD operations
- API key authentication
- Role-based authorization
- Ownership validation
- Timestamp fields
- Filtering support
- Pagination support
- Task workflow/state transitions
- OpenAPI contract tests
- Smoke tests
- Regression tests
- Database-backed integration tests
- Test helpers and fixtures
- GitHub Actions CI
- Black formatting checks
- Flake8 linting
- HTML test reports

---

# In Progress / Future Ideas

- PostgreSQL support
- Alembic migrations
- Docker validation
- Expanded OpenAPI schema validation
- Additional edge-case automation coverage
- Enhanced reporting and dashboards

---

# Why I Built This Project

I created this project to strengthen both my backend development and QA automation skills.

Rather than only testing existing applications, I wanted experience building an API, understanding how features are implemented, and then writing automated tests to verify those features.

The project helped me gain experience with:

- API development
- Database integration
- Automated testing
- CI/CD workflows
- Debugging real-world integration issues

---

# Key Learning Outcomes

Some of the most valuable lessons from this project included:

- Designing and testing REST APIs
- Working with relational databases
- Modeling relationships between resources
- Writing maintainable automated tests
- Building and validating OpenAPI contracts
- Troubleshooting authentication and authorization issues
- Debugging database-related failures
- Keeping tests aligned with changing application behavior
- Using CI pipelines to automate quality checks

---

# Author

Created by **Todd Nason** as a QA Automation portfolio project.