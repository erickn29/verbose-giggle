import uuid

import pytest

from apps.v1.interview.model import Chat
from apps.v1.interview.repository import ChatRepository
from apps.v1.user.repository import UserRepository


@pytest.fixture(scope="session")
async def chats(session):
    user_repository = UserRepository(session)
    chat_repository = ChatRepository(session)

    user = await user_repository.create(
        email="user@chat.com",
        password="user@user.com",
    )
    chat_to_upd = await chat_repository.create(
        user_id=user.id,
        title="repository_test_chat_chat_1",
        config={},
    )
    chat_to_del = await chat_repository.create(
        user_id=user.id,
        title="repository_test_chat_chat_2",
        config={},
    )

    return {"user": user, "chat_to_upd": chat_to_upd, "chat_to_del": chat_to_del}


async def test_get(session, chats):
    async with session:
        chat_repository = ChatRepository(session)
        chat = await chat_repository.get(chats["chat_to_upd"].id)
        assert isinstance(chat, Chat)
        assert chat.id == chats["chat_to_upd"].id


async def test_create(session, chats):
    async with session:
        chat_repository = ChatRepository(session)
        chat = await chat_repository.create(
            user_id=chats["user"].id, title="test_chat", config={}
        )
        assert chat.id is not None
        assert chat.user_id == chats["user"].id
        assert chat.title == "test_chat"

        obj_chat = await chat_repository.get(chat.id)
        if not obj_chat:
            raise AssertionError("Chat not found")

        assert obj_chat.user_id == chats["user"].id
        assert obj_chat.title == "test_chat"


async def test_update(session, chats):
    async with session:
        chat_repository = ChatRepository(session)
        chat = await chat_repository.get(chats["chat_to_upd"].id)
        assert chat
        await chat_repository.update(
            chat,
            title="updated_chat",
        )
        chat = await chat_repository.get(chats["chat_to_upd"].id)
        assert chat
        assert chat.title == "updated_chat"
        assert chat.user_id == chats["user"].id


async def test_delete(session, chats):
    async with session:
        chat_repository = ChatRepository(session)
        chat = await chat_repository.get(chats["chat_to_del"].id)
        assert chat

        await chat_repository.delete(chat)
        chat = await chat_repository.get(chats["chat_to_del"].id)
        assert chat is None


async def test_all(session, chats):
    async with session:
        chat_repository = ChatRepository(session)
        chats = await chat_repository.all()
        assert len(chats) >= 1


async def test_count(session, chats):
    async with session:
        chat_repository = ChatRepository(session)
        chats_count = await chat_repository.count(
            {
                "user_id": chats["user"].id,
            }
        )
        assert isinstance(chats_count, int)
        assert chats_count >= 1


async def test_exists_true(session, chats):
    async with session:
        chat_repository = ChatRepository(session)
        is_exists = await chat_repository.exists({"user_id": chats["user"].id})
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        chat_repository = ChatRepository(session)
        is_exists = await chat_repository.exists({"user_id": uuid.uuid4()})
        assert is_exists is False
