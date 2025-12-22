import uuid

from app.schemas.user import UserRead
from app.dependencies.user_dependencies import get_user_service


class TestListUsers:
    """Test list_uses endpoint"""

    def test_list_users_default_params(self, mocker, app, client):
        """Case: list users with default limit and offset"""
        mock_service = mocker.Mock()
        mock_service.list_users.return_value = [
            UserRead(
                id=uuid.uuid4(),
                email="user1@mail.com",
                full_name="User 1",
                is_active=True,
            ),
            UserRead(
                id=uuid.uuid4(),
                email="user2@mail.com",
                full_name="User 2",
                is_active=True,
            ),
        ]
        app.dependency_overrides[get_user_service] = lambda: mock_service

        response = client.get("/users/")

        assert response.status_code == 200
        assert len(response.json()) == 2
        mock_service.list_users.assert_called_once_with(limit=10, offset=0)
