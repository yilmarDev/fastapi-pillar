from contextlib import asynccontextmanager
from typing import Dict
from fastapi import FastAPI
from app.config.settings import get_settings
from app.routers.users import router as users_router
from app.db.database import create_db_and_tables, postgres_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    postgres_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "FastAPI Pillar is running!"}


@app.get(
    "/environment",
    responses={
        200: {
            "description": "Current environment configuration",
            "content": {
                "application/json": {
                    "example": {"environment": "development", "status": "active"}
                }
            },
        }
    },
)
def get_current_environment() -> Dict[str, str]:
    settings = get_settings()
    return {"environment": settings.env, "status": "active"}


@app.get(
    "/greeting/{name}",
    responses={
        200: {
            "description": "Current environment configuration",
            "content": {
                "application/json": {
                    "example": {"greet": "Hello Daniel", "status": "200"}
                }
            },
        }
    },
)
def greet(name: str) -> Dict[str, str]:
    settings = get_settings()
    return {"greet": f"Hello {name}", "status": "200"}
