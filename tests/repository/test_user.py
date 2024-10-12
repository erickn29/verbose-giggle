import pytest

from apps.v1.user.repository import UserRepository


@pytest.fixture(scope="session")
async def users(session):
    user_repository = UserRepository(session)
    user_to_del = await user_repository.create(
        email="test_email@example.com",
        password="test_password",
    )
    user_to_update = await user_repository.create(
        email="test_email_update@example.com",
        password="test_password_update",
    )

    return {
        "user_to_del": user_to_del,
        "user_to_update": user_to_update,
    }


async def test_get(session, users):
    async with session:
        user_repository = UserRepository(session)
        user = await user_repository.get(users["user_to_update"].id)
        if not user:
            raise AssertionError("User not found")
        assert user.id == users["user_to_update"].id


async def test_create(session, users):
    async with session:
        user_repository = UserRepository(session)
        user = await user_repository.create(
            email="test_email_2@example.com",
            password="test_password_2",
        )
        assert user.id is not None
        assert user.email == "test_email_2@example.com"
        assert user.password == "test_password_2"

        user_obj = await user_repository.get(user.id)
        if not user_obj:
            raise AssertionError("User not found")
        assert user_obj.email == "test_email_2@example.com"
        assert user_obj.password == "test_password_2"


async def test_update(session, users):
    async with session:
        user_repository = UserRepository(session)
        user = await user_repository.get(users["user_to_update"].id)
        if not user:
            raise AssertionError("User not found")
        await user_repository.update(user, email="updated_email@example.com")
        user_obj = await user_repository.get(user.id)
        if not user_obj:
            raise AssertionError("User not found")
        assert user_obj.email == "updated_email@example.com"


async def test_delete(session, users):
    async with session:
        user_repository = UserRepository(session)
        user = await user_repository.get(users["user_to_del"].id)
        if not user:
            raise AssertionError("User not found")
        await user_repository.delete(user)
        user_obj = await user_repository.get(user.id)
        assert user_obj is None
