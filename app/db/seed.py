from app.factories.user_factory import UserFactory
from app.config.settings import get_settings

settings = get_settings()


def seed_users(count: int = 10) -> None:
    """
    Generate users in DB

    Args:
        count: ammount of users to create (default: 10)
    """
    print("Seeding users...")
    print(f"Env: {settings.env}")
    print(f"Generating {count} users...")

    try:
        # Creating users
        users = []
        for i in range(count):
            user = UserFactory.create()
            users.append(user)
            if (i + 1) % 10 == 0:
                print(f"   ... {i + 1}/{count} users created")

        print(f"{len(users)} users created!")
        print(f"Example: {users[0].email if users else 'N/A'}")

    except Exception as e:
        print(f"Error while seeding: {e}")
        raise


def run() -> None:
    """Ejecuta todos los seeds"""

    # Validating environment
    if settings.env == "production":
        print("WARNING: Seed cannot be run in production")
        return

    print("=" * 50)
    print("Starting seed process")
    print("=" * 50)

    seed_users(count=30)

    print("=" * 50)
    print("Seed completed!")
    print("=" * 50)


if __name__ == "__main__":
    run()
