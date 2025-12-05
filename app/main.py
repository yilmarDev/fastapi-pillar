from fastapi import FastAPI
from app.config.settings import get_settings

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI base challenge is running!"}


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
def get_current_environment():
    settings = get_settings()
    return {"environment": settings.env, "status": "active"}


@app.get(
    "/greeting",
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
def greet():
    settings = get_settings()
    return {"greet": "Hellow Man", "status": "200"}
