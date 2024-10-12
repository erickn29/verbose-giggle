from utils.mail import Mail


async def test_password_reset_request_success(client, auth_headers, mocker):
    mock_response = mocker.patch.object(Mail, "send_email")
    mock_response.return_value = None
    response = await client.post(
        "/api/v1/auth/password-reset/",
        json={"email": auth_headers["user"].email},
    )
    assert response.status_code == 200
    assert response.json()["status"] is True


async def test_password_reset_request_bad_email(client, auth_headers, mocker):
    mock_response = mocker.patch.object(Mail, "send_email")
    mock_response.return_value = None
    response = await client.post(
        "/api/v1/auth/password-reset/",
        json={"email": "bad@email.com"},
    )
    assert response.status_code == 200
    assert response.json()["status"] is False


async def test_password_reset_request_422(client, auth_headers, mocker):
    mock_response = mocker.patch.object(Mail, "send_email")
    mock_response.return_value = None
    response = await client.post(
        "/api/v1/auth/password-reset/",
        json={"emaill": auth_headers["user"].email},
    )
    assert response.status_code == 422
