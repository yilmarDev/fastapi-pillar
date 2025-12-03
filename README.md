# FastAPI Clean Architecture Base Project

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

- **Python 3.14**
- **FastAPI**
- **SQLModel**
- **PostgreSQL**
- **Docker & Docker Compose**
- **Pytest** (async support with `httpx` + `ASGITransport`)
- **Faker** (for seeds)
- **Alembic** (migrations)
- **CircleCI** (CI pipeline)
- **Coverage + Coveralls**
- **OAuth2 with Google** (optional module)
- **Black & Ruff** (linting and formatting)
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

Run tests:

```shell
# Local tests
pytest -v

# Run with coverage:
pytest --cov=app
```

## 🐳 Docker Setup

```sh
# Start the complete development environment:
docker-compose up -d

# Build the backend image:
docker build -t fastapi-clean .

# Run locally
docker run -p 8000:8000 fastapi-clean
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

Planned CI/CD features:

- CircleCI pipeline for automated testing
- Coverage reporting (Coveralls)
- Dockerized builds
- Deployment workflows for:
  - Heroku
  - Vercel serverless functions
  - AWS (Lambda or ECS)

## ▶️ How to Run Locally

Install dependencies:

```sh
# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload
```

## API documentation:

- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc

## 📄 License

This project is released under the MIT License.
