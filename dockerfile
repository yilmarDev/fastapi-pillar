# Stage 1: Builder
FROM python:3.14-slim AS builder

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
COPY requirements.txt .

# Install dependencies in specific prefix
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy application code and necessary files
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./tests /app/tests
COPY pytest.ini /app/
COPY pyproject.toml /app/
COPY alembic.ini /app/


# Stage 2: Runtime
FROM python:3.14-slim

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
COPY --from=builder --chown=appuser:appuser /install /usr/local

# Copy application code and all necessary files with correct permissions
COPY --from=builder --chown=appuser:appuser /app /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Default command (overridden in docker-compose for development)
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]