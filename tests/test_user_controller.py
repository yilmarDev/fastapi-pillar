from app.schemas.user import UserCreate, UserRead
from app.dependencies.user_dependencies import get_user_service
from app.services.user_service import UserService


class TestUserController:
    """Integration test for user endpoints"""

    def test_create_user(self, client, db_session, app):
        """Test create user - Real integration with test db"""
        payload = UserCreate(
            email="newuser@mail.com",
            password="securepass1234",
            full_name="New user name",
        )

        response = client.post("/users/", json=payload.model_dump())

        assert response.status_code == 200
        db_session.commit()
