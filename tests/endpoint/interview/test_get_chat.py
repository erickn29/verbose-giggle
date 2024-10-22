import uuid

import pytest

from apps.v1.interview.service import ChatService, MessageService


@pytest.fixture(scope="session")
async def chats(session, auth_headers):
    chat_service = ChatService(session)
    message_service = MessageService(session)

    chat_to_upd = await chat_service.create(
        user_id=auth_headers["user"].id,
        title="test_chat_to_upd",
        config={"technologies": [{"technology": "php", "complexity": "easy"}]},
    )
    chat_to_del = await chat_service.create(
        user_id=auth_headers["user"].id,
        title="test_chat_to_del",
        config={"technologies": [{"technology": "php", "complexity": "easy"}]},
    )

    await message_service.create(
        chat_id=chat_to_upd.id,
        text="test_message_1",
        type="question",
    )
    await message_service.create(
        chat_id=chat_to_upd.id,
        text="test_message_2",
        type="answer",
    )

    return {"chat_to_upd": chat_to_upd, "chat_to_del": chat_to_del}


async def test_get_chat_200(session, auth_headers, client, chats):
    await session.refresh(chats["chat_to_upd"])
    response = await client.get(
        f"api/v1/interview/chat/{str(chats['chat_to_upd'].id)}/",
        headers=auth_headers["auth_headers"],
    )
    assert response.status_code == 200
    assert response.json()["id"] == str(chats["chat_to_upd"].id)
    assert response.json()["title"] == "test_chat_to_upd"
    assert response.json()["config"]["technologies"][0]["technology"] == "php"
    assert len(response.json()["messages"]) == 2
    assert response.json()["messages"][0]["text"] == "test_message_1"
    assert response.json()["messages"][1]["text"] == "test_message_2"


async def test_get_chat_401(auth_headers, client, chats):
    response = await client.get(
        f"api/v1/interview/chat/{str(chats['chat_to_upd'].id)}/",
        # headers=auth_headers["auth_headers"],
    )
    assert response.status_code == 401


async def test_get_chat_403_wrong_user(auth_headers, client, chats):
    response = await client.get(
        f"api/v1/interview/chat/{str(chats['chat_to_upd'].id)}/",
        headers=auth_headers["auth_headers2"],
    )
    assert response.status_code == 403
    assert response.json()["msg"] == "Доступ запрещен"


async def test_get_chat_403_no_verified_email(auth_headers, client, chats):
    response = await client.get(
        f"api/v1/interview/chat/{str(chats['chat_to_upd'].id)}/",
        headers=auth_headers["auth_headers3"],
    )
    assert response.status_code == 403
    assert response.json()["msg"] == "Необходимо подтвердить email"


async def test_get_chat_404(auth_headers, client, chats):
    response = await client.get(
        f"api/v1/interview/chat/{str(uuid.uuid4())}/",
        headers=auth_headers["auth_headers"],
    )
    assert response.status_code == 404
