import pytest

from apps.v1.user.service import UserService


@pytest.fixture(scope="session")
async def users(session):
    user_service = UserService(session)
    user_to_del = await user_service.create(
        email="test_email@example_service.com",
        password="test_password",
    )
    user_to_update = await user_service.create(
        email="test_email_update@example_service.com",
        password="test_password_update",
    )

    return {
        "user_to_del": user_to_del,
        "user_to_update": user_to_update,
    }


async def test_get(session, users):
    async with session:
        user_service = UserService(session)
        user = await user_service.get(users["user_to_update"].id)
        if not user:
            raise AssertionError("User not found")
        assert user.id == users["user_to_update"].id


async def test_create(session, users):
    async with session:
        user_service = UserService(session)
        user = await user_service.create(
            email="test_email_2@example_service.com",
            password="test_password_2",
        )
        assert user.id is not None
        assert user.email == "test_email_2@example_service.com"
        assert user.password != "test_password_2"

        user_obj = await user_service.get(user.id)
        if not user_obj:
            raise AssertionError("User not found")
        assert user_obj.email == "test_email_2@example_service.com"
        assert user_obj.password != "test_password_2"


async def test_update(session, users):
    async with session:
        user_service = UserService(session)
        user = await user_service.get(users["user_to_update"].id)
        if not user:
            raise AssertionError("User not found")
        await user_service.update(user, email="updated_email@example_service.com")
        user_obj = await user_service.get(user.id)
        if not user_obj:
            raise AssertionError("User not found")
        assert user_obj.email == "updated_email@example_service.com"


async def test_delete(session, users):
    async with session:
        user_service = UserService(session)
        user = await user_service.get(users["user_to_del"].id)
        if not user:
            raise AssertionError("User not found")
        await user_service.delete(user)
        user_obj = await user_service.get(user.id)
        assert user_obj is None
