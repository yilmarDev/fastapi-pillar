"""
User-related dependency injection factories.

This module provides factory functions for creating UserService instances
with all their dependencies properly wired up.
"""

from typing import Generator

from fastapi import Depends
from sqlmodel import Session

from app.db.database import postgres_client
from app.respositories.user_repository import UserRepository
from app.services.user_service import UserService


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session.
    This is the dependency that will be overridden in tests.
    """
    with postgres_client.get_session_context() as session:
        yield session


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """
    Factory function for UserService dependency injection.

    Creates the complete dependency chain:
    Session -> UserRepository -> UserService

    This is the Composition Root for user-related operations.
    Controllers should depend on this function via FastAPI's Depends().

    Args:
        db: Database session (injected by FastAPI)

    Returns:
        UserService: Fully configured service instance
    """
    repo = UserRepository(db)
    return UserService(repo)
