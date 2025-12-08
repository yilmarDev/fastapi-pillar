import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


class TestUserCreate:
    """Test to validate UserCreate schema"""

    def test_valid_user_create(self):
        """Case: valid email and password"""
        data = {
            "email": "testuser@mail.com",
            "password": "pass-0001",
            "full_name": "Test user",
        }

        user = UserCreate(**data)

        assert user.email == "testuser@mail.com"
        assert user.password == "pass-0001"
        assert user.full_name == "Test user"

    def test_invalid_email_user_create(self):
        """Case: invalid user email"""
        data = {
            "email": "testuser",
            "password": "pass-0001",
            "full_name": "Test user",
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_invalid_password_user_create(self):
        """Case: invalid user email"""
        data = {
            "email": "testuser@mail.com",
            "password": "",
            "full_name": "Test user",
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_extra_fields_rejected(self):
        """ "Case: extra fields rejected"""

        data = {
            "email": "testuser@mail.com",
            "password": "pass-0001",
            "full_name": "Test user",
            "extra_info": "More info",
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_optional_full_name(self):
        """Case: No full name"""

        data = {
            "email": "testuser@mail.com",
            "password": "pass-0001",
        }

        user = UserCreate(**data)
        assert user.email == "testuser@mail.com"
