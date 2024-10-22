import pytest

from apps.v1.interview.service import ChatService


@pytest.fixture(scope="session")
async def chats(session, auth_headers):
    chat_service = ChatService(session)

    chat1 = await chat_service.create(
        user_id=auth_headers["user4"].id,
        title="test_chat1",
        config={"technologies": [{"technology": "php", "complexity": "easy"}]},
    )
    chat2 = await chat_service.create(
        user_id=auth_headers["user4"].id,
        title="test_chat2",
        config={"technologies": [{"technology": "php", "complexity": "easy"}]},
    )

    return {"chat1": chat1, "chat2": chat2}


async def test_get_chats_200(session, auth_headers, client, chats):
    response = await client.get(
        "api/v1/interview/chat/", headers=auth_headers["auth_headers4"]
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
    assert response.json()["items"][0]["id"] == str(chats["chat2"].id)
    assert response.json()["items"][1]["id"] == str(chats["chat1"].id)


async def test_get_chats_401(session, auth_headers, client, chats):
    response = await client.get("api/v1/interview/chat/")
    assert response.status_code == 401


async def test_get_chats_403(session, auth_headers, client, chats):
    response = await client.get(
        "api/v1/interview/chat/", headers=auth_headers["auth_headers3"]
    )
    assert response.status_code == 403
