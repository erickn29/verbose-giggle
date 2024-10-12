import pytest

from apps.v1.user.service import UserService


@pytest.fixture(scope="session")
async def user(session):
    user_service = UserService(session)
    user = await user_service.create(
        email="user1@example_auth.com",
        password="test_password",
    )
    return user


async def test_login_success(session, user, client):
    data = {
        "email": user.email,
        "password": "test_password",
    }
    response = await client.post(
        "/api/v1/auth/login/",
        json=data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


async def test_login_validation_error(session, user, client):
    data = {
        "email": user.email,
        # "password": "test_password",
    }
    response = await client.post(
        "/api/v1/auth/login/",
        json=data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


async def test_login_wrong_password(session, user, client):
    data = {
        "email": user.email,
        "password": "test_password2",
    }
    response = await client.post(
        "/api/v1/auth/login/",
        json=data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 401
    assert (
        "Некорректные имя пользователя или пароль" in response.json()["extra"]["detail"]
    )


async def test_login_wrong_email(session, user, client):
    data = {
        "email": user.email + "xxx",
        "password": "test_password",
    }
    response = await client.post(
        "/api/v1/auth/login/",
        json=data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 401
    assert (
        "Некорректные имя пользователя или пароль" in response.json()["extra"]["detail"]
    )
