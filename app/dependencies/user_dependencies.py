"""
User-related dependency injection factories.

This module provides factory functions for creating UserService instances
with all their dependencies properly wired up.
"""

from app.db.database import postgres_client
from app.services.user_service import UserService
from app.respositories.user_repository import UserRepository


def get_user_service() -> UserService:
    """
    Factory function for UserService dependency injection.

    Creates the complete dependency chain:
    PostgresClient -> UserRepository -> UserService

    This is the Composition Root for user-related operations.
    Controllers should depend on this function via FastAPI's Depends().

    Returns:
        UserService: Fully configured service instance
    """
    repo = UserRepository(postgres_client)
    return UserService(repo)
