from uuid import uuid4

from factory.declarations import LazyAttribute, LazyFunction
from faker import Faker

from app.core.security import get_hash_password
from app.models.user import User

from .base import BaseFactory

fake = Faker()


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = LazyFunction(uuid4)
    email = LazyAttribute(lambda _: fake.unique.email())
    full_name = LazyAttribute(lambda _: fake.name())
    is_active = True
    hashed_password = LazyFunction(lambda: get_hash_password("password123"))
