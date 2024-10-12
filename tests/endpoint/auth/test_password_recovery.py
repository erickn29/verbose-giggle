import datetime
import uuid

from apps.v1.auth.service import RecoveryTokenService
from apps.v1.user.service import UserService


async def test_password_recovery_success(session, client, auth_headers):
    recovery_service = RecoveryTokenService(session=session)
    token, _ = await recovery_service.create(
        token=uuid.uuid4().hex,
        user_id=auth_headers["user"].id,
    )

    data = {"token": token.token, "password": auth_headers["user"].email}
    response = await client.post(
        "/api/v1/auth/password-recovery/",
        json=data,
    )
    assert response.status_code == 200
    assert response.json()["status"] is True

    user_service = UserService(session)
    user_obj = await user_service.get(auth_headers["user"].id)
    if not user_obj:
        raise AssertionError("User not found")
    assert user_obj.password != auth_headers["user"].password


async def test_password_recovery_bad_token(session, client, auth_headers):
    recovery_service = RecoveryTokenService(session=session)
    token, _ = await recovery_service.create(
        token=uuid.uuid4().hex,
        user_id=auth_headers["user"].id,
    )

    data = {"token": uuid.uuid4().hex, "password": auth_headers["user"].email}
    response = await client.post(
        "/api/v1/auth/password-recovery/",
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["extra"]["detail"] == "Токен не найден"


async def test_password_recovery_token_expired(session, client, auth_headers):
    recovery_service = RecoveryTokenService(session=session)
    token, _ = await recovery_service.create(
        token=uuid.uuid4().hex,
        user_id=auth_headers["user"].id,
        created_at=datetime.datetime(1999, 1, 1),
    )

    data = {"token": token.token, "password": auth_headers["user"].email}
    response = await client.post(
        "/api/v1/auth/password-recovery/",
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["extra"]["detail"]
        == "Токен использован или срок использования истек"
    )


async def test_password_recovery_token_used(session, client, auth_headers):
    recovery_service = RecoveryTokenService(session=session)
    token, _ = await recovery_service.create(
        token=uuid.uuid4().hex,
        user_id=auth_headers["user"].id,
        is_used=True,
    )

    data = {"token": token.token, "password": auth_headers["user"].email}
    response = await client.post(
        "/api/v1/auth/password-recovery/",
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["extra"]["detail"]
        == "Токен использован или срок использования истек"
    )
