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
    
    
async def test_create_chat_422(client, auth_headers):
    response = await client.post(
        "/api/v1/interview/chat/",
        headers=auth_headers["auth_headers"],
        json={
            "title": "test_chat", 
            # "config": {
            #     "technologies": [{"technology": "php", "complexity": "hard"}]
            # }
        },
    )
    assert response.status_code == 422
    
    
async def test_create_chat_401(client, auth_headers):
    response = await client.post(
        "/api/v1/interview/chat/",
        # headers=auth_headers["auth_headers"],
        json={
            "title": "test_chat", 
            "config": {
                "technologies": [{"technology": "php", "complexity": "hard"}]
            }
        },
    )
    assert response.status_code == 401
    
    
async def test_create_chat_403(client, auth_headers):
    response = await client.post(
        "/api/v1/interview/chat/",
        headers=auth_headers["auth_headers3"],
        json={
            "title": "test_chat", 
            "config": {
                "technologies": [{"technology": "php", "complexity": "hard"}]
            }
        },
    )
    assert response.status_code == 403
    