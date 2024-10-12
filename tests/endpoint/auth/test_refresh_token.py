async def test_refresh_token_success(client, auth_headers):
    response = await client.post(
        "/api/v1/auth/token/refresh/", json={"token": auth_headers["refresh_token"]}
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


async def test_refresh_token_bad_token(client, auth_headers):
    response = await client.post(
        "/api/v1/auth/token/refresh/", json={"token": "bad_token"}
    )
    assert response.status_code == 401


async def test_refresh_token_validation_error(client, auth_headers):
    response = await client.post(
        "/api/v1/auth/token/refresh/", json={"tokeN": auth_headers["refresh_token"]}
    )
    assert response.status_code == 422
