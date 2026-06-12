# Stage 1: Builder (production dependencies)
FROM python:3.13-slim AS builder

# Environment variables to optimize build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies for compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first (leverage Docker cache)
COPY pyproject.toml ./

# Create minimal structure for package installation
RUN echo "# FastAPI Pillar" > README.md && \
    mkdir -p app && \
    touch app/__init__.py

# Install production dependencies in specific prefix
RUN pip install uv && \
    uv pip install --system .

# Copy application code and necessary files
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./tests /app/tests
COPY .coveragerc /app/
COPY pytest.ini /app/
COPY pyproject.toml /app/
COPY alembic.ini /app/

# Stage 1b: Builder with dev dependencies (for testing)
FROM builder AS builder-test

# Install dev dependencies on top of production ones
RUN uv pip install --system --group dev .

# Stage 2: Runtime
FROM python:3.13-slim

# Runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime dependencies for PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Copy installed dependencies with correct permissions
COPY --from=builder --chown=appuser:appuser /usr/local /usr/local

# Copy application code and all necessary files with correct permissions
COPY --from=builder --chown=appuser:appuser /app /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Default command (overridden in docker-compose for development)
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

# Stage 3: Test runtime (with dev dependencies)
FROM python:3.13-slim AS test

# Runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime dependencies for PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed dependencies including dev dependencies
COPY --from=builder-test /usr/local /usr/local

# Copy application code and test files
COPY --from=builder-test /app /app

# Default command for tests
CMD ["pytest", "--verbose", "--tb=short"]