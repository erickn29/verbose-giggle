async def test_create_chat_201(client, auth_headers):
    response = await client.post(
        "/api/v1/interview/chat/",
        headers=auth_headers["auth_headers"],
        json={
            "title": "test_chat", 
            "config": {
                "technologies": [{"technology": "php", "complexity": "hard"}]
            }
        },
    )
    assert response.status_code == 201
    assert response.json()["title"] == "test_chat"
    assert response.json()["id"]
    assert response.json()["config"]["technologies"][0]["technology"] == "php"