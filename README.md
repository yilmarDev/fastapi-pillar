# FastAPI Clean Architecture Base Project

[![Tests](https://github.com/yilmarDev/fastapi-pillar/workflows/lint%20and%20test/badge.svg)](https://github.com/yilmarDev/fastapi-pillar/actions)
[![codecov](https://codecov.io/github/yilmarDev/fastapi-pillar/graph/badge.svg?token=7UV76FAKT4)](https://codecov.io/github/yilmarDev/fastapi-pillar)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.123-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192.svg?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg?logo=docker)](https://www.docker.com/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A production-ready **FastAPI** backend boilerplate designed with clean architecture principles, modern best practices, and full support for testing, containerization, CI/CD, and scalable development.

This project can be used as a starting point for real-world applications, technical assessments, microservices, or backend services consumed by frontend/mobile applications.

---

## 🚀 Features

### 🔹 Architecture

The project follows an adapted **Clean Architecture** with clear separation of concerns:

- **Controllers** – Request handlers and routing
- **Services** – Business logic
- **Repositories** – Data access layer
- **Clients** – Database and external API clients
- **Wrappers** – Optional abstraction layer to switch data sources
- **Models / Schemas** – SQLModel ORM models and Pydantic schemas
- **Core** – Configuration, utilities, middleware, and security
- **Config** – Environment variables and application settings

---

## 🧱 Technology Stack

- **Python 3.13**
- **FastAPI**
- **SQLModel**
- **PostgreSQL**
- **Docker & Docker Compose**
- **Pytest** (async support with `httpx` + `ASGITransport`)
- **Faker** (for seeds)
- **Alembic** (migrations)
- **GitHub Actions** (CI/CD pipeline)
- **Coverage + Codecov**
- **OAuth2 with Google** (optional module)
- **uv** (dependency management)
- **Ruff** (linting and formatting)
- **Dotenv** (environment configuration)

---

## 🧪 Testing

The project uses modern async testing patterns:

- `pytest`
- `pytest-asyncio`
- `httpx` with `ASGITransport`
- A dedicated **PostgreSQL test database** (Docker)

Example basic test:

```python
async with AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
) as ac:
    response = await ac.get("/")
```

### Running Tests Locally

```shell
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_user_schemas.py -v

# Run tests matching a pattern
pytest -k "test_user" -v

# Run tests with coverage report
coverage run -m pytest

# Display coverage in terminal
coverage report

# Generate HTML coverage report
coverage html

# View HTML report
open coverage_html_report/index.html
```

### Running Tests in Docker

```shell
# Run all tests with coverage in Docker
docker compose run test

# Run tests and generate HTML coverage report
docker compose run test coverage html
```

**Note:** The `test` service runs automatically with:

- All tests executed (`pytest`)
- Coverage measurement enabled
- Minimum 80% coverage threshold enforced
- HTML report generated in `coverage_html_report/`

### Code Coverage

This project uses **Coverage.py** to measure code quality:

**Coverage Configuration** (`.coveragerc`):

- Source: `app/` directory
- Minimum threshold: **80%**
- Branch coverage enabled
- Excludes: `__init__.py` files and venv
- Data file: `/tmp/.coverage` (persists in container temp)

The coverage report shows:

- **Line coverage**: % of lines executed
- **Branch coverage**: % of conditional branches tested
- **Missing lines**: which code wasn't tested

## ⚙️ Environment Configuration

Copy the example environment file and configure your settings:

```sh
cp .env.example .env
```

Edit `.env` with your specific configuration. The `.env.example` file includes:

- Database URLs for Docker and local development
- Environment variables
- Optional API keys and secrets

## 🐳 Docker Setup (Recommended)

> **⚠️ Recommended Approach:** This project is designed to run in Docker. Using Docker ensures consistency across environments and simplifies dependency management.

This project uses **Docker Compose** to orchestrate the complete development environment with:

- FastAPI application with hot-reload
- PostgreSQL (main database)
- PostgreSQL (test database)

### Start Development Environment

```sh
# Start all services (app + databases)
docker compose up

# Or run in background
docker compose up -d

# View logs
docker compose logs -f app

# Stop all services
docker compose down
```

### Features

✅ **Hot-reload enabled** - Code changes are automatically detected  
✅ **Persistent databases** - Data is preserved between restarts  
✅ **Isolated test database** - Tests don't affect development data  
✅ **Automatic user permissions** - Files created match your local user

### Access the API

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Main Database: `localhost:5488`
- Test Database: `localhost:5489`

### Rebuild After Changes

```sh
# Rebuild images after Dockerfile or pyproject.toml changes
docker compose up --build

# Completely reset (removes volumes)
docker compose down -v
```

<!-- ## 📦 Project Structure

challenge/
│── app/
│ ├── core/
│ ├── controllers/
│ ├── services/
│ ├── repositories/
│ ├── clients/
│ ├── wrappers/
│ ├── models/
│ ├── schemas/
│ ├── config/
│ └── main.py
│
│── tests/
│── .env
│── Dockerfile
│── docker-compose.yml
│── pyproject.toml
│── README.md -->

## 👤 User Module (Planned)

A flexible and extensible user module featuring:

- Base User model
- Extensible profiles:
- Customer
- Provider
- Seller
- Administrator
- Optional authentication via Google OAuth

## 📡 External API Integration

The project includes a pattern for interacting with external APIs:

- Dedicated client layer
- Optional retry logic and caching
- Mocked clients for testing

## 🔄 CI/CD

CI/CD features:

- GitHub Actions pipeline for automated testing
- Coverage reporting (Codecov)
- Automated linting and formatting checks
- Dockerized builds
- Ready for deployment to:
  - Heroku
  - Vercel serverless functions
  - AWS (Lambda or ECS)

## ▶️ How to Run Locally (Without Docker)

> **Note:** Running with Docker (see above) is the recommended approach. This section is for advanced users who prefer local development.

### Prerequisites

You need **PostgreSQL** running locally. Choose one of these options:

#### Option 1: Use Docker for databases only (Recommended)

```sh
# Start only the databases
docker compose up postgres_main postgres_test -d

# Your app will connect to these databases on:
# - Main DB: localhost:5488
# - Test DB: localhost:5489
```

#### Option 2: Install PostgreSQL locally

```sh
# macOS (using Homebrew)
brew install postgresql@16
brew services start postgresql@16

# Create databases
createdb fastapi_pillar
createdb fastapi_pillar_test
```

### Run the Application

```sh
# Install dependencies and create virtual environment
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Configure environment variables (create .env file)
# DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5488/fastapi_pillar
# TEST_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5489/fastapi_pillar_test

# Run database migrations
alembic upgrade head

# Start the API
fastapi dev app/main.py
```

### API Documentation

- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc

---

## 🗃️ Database Migrations

This project uses **Alembic** for database migrations.

### Creating a New Migration

When you modify models (add/remove fields, create new tables):

```sh
# Generate migration automatically (Alembic detects changes)
alembic revision --autogenerate -m "Description of changes"

# Example:
alembic revision --autogenerate -m "Add phone field to User"
```

### Applying Migrations

```sh
# Apply all pending migrations
alembic upgrade head

# Apply one migration at a time
alembic upgrade +1
```

### Rolling Back Migrations

```sh
# Rollback last migration
alembic downgrade -1

# Rollback to a specific version
alembic downgrade <revision_id>
```

### Useful Alembic Commands

```sh
# Show current migration version
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --verbose
```

### Important Notes

- **Always review** auto-generated migrations before applying them
- The migration files are in `alembic/versions/`
- Both development and test databases need migrations applied
- In Docker, migrations run automatically on container start

---

## 🌱 Database Seeding

The project includes a seeding system to populate your database with fake data for development and testing.

### Features

- Generates realistic fake users using **Faker** and **Factory Boy**
- Safety check: prevents accidental seeding in production
- Progress tracking and informative console output
- Easily extensible for additional models

### Running the Seed

From the **project root directory**:

```sh
# Run the seed script (creates 10 users by default)
python -m app.db.seed
```

### Customizing Seed Data

You can modify `app/db/seed.py` to:

- Change the number of users created
- Add seeds for other models
- Customize fake data generation

Example programmatic usage:

```python
from app.db.seed import seed_users

# Create 50 users
seed_users(count=50)
```

### Seed Configuration

The seed uses the factory configuration from `app/factories/`:

- **Development**: Uses your main database
- **Test environment**: Automatically uses test database
- **Production**: Blocked by safety check

Default credentials for seeded users:

- Password: `password123` (hashed with bcrypt)

---

## 📄 License

This project is released under the MIT License.
