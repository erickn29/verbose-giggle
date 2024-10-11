import datetime
import uuid

import pytest

from apps.v1.interview.model import Message
from apps.v1.interview.repository import ChatRepository, MessageRepository
from apps.v1.interview.schema import MessageType
from apps.v1.user.repository import UserRepository


@pytest.fixture(scope="session")
async def messages(session):
    user_repository = UserRepository(session)
    chat_repository = ChatRepository(session)
    message_repository = MessageRepository(session)

    user = await user_repository.create(
        email="user@message.com",
        password="user@user.com",
    )
    chat = await chat_repository.create(
        user_id=user.id,
        title="repository_test_message_chat_1",
        config={},
    )
    message_to_upd = await message_repository.create(
        chat_id=chat.id,
        text="repository_test_message_message_1",
        type=MessageType.ANSWER.value,
    )
    message_to_upd2 = await message_repository.create(
        chat_id=chat.id,
        text="repository_test_message_message_12",
        type=MessageType.ANSWER.value,
    )
    message_to_del = await message_repository.create(
        chat_id=chat.id,
        text="repository_test_message_message_2",
        type=MessageType.ANSWER.value,
    )
    await message_repository.create(
        chat_id=chat.id,
        text="repository_test_message_message_filter_1",
        type=MessageType.ANSWER.value,
        created_at=datetime.date(2024, 9, 1),
    )
    await message_repository.create(
        chat_id=chat.id,
        text="repository_test_message_message_filter_2",
        type=MessageType.ANSWER.value,
        created_at=datetime.date(2024, 9, 3),
    )
    await message_repository.create(
        chat_id=chat.id,
        text="repository_test_message_message_filter_3",
        type=MessageType.QUESTION.value,
        created_at=datetime.date(2024, 9, 5),
    )

    return {
        "user": user,
        "chat": chat,
        "message_to_upd": message_to_upd,
        "message_to_upd2": message_to_upd2,
        "message_to_del": message_to_del,
    }
    
    
async def test_get(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        message = await message_repository.get(messages["message_to_upd"].id)
        assert isinstance(message, Message)
        assert message.id == messages["message_to_upd"].id


async def test_create(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        message = await message_repository.create(
            chat_id=messages["chat"].id,
            text="test_message",
            type=MessageType.EVALUATION.value,
        )
        assert message.id is not None
        assert message.chat_id == messages["chat"].id
        assert message.text == "test_message"
        assert message.type == MessageType.EVALUATION.value

        obj_message = await message_repository.get(message.id)
        if not obj_message:
            raise AssertionError("Message not found")

        assert obj_message.chat_id == messages["chat"].id
        assert obj_message.text == "test_message"
        assert obj_message.type == MessageType.EVALUATION.value


async def test_update(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        message = await message_repository.get(messages["message_to_upd"].id)
        assert message
        await message_repository.update(
            message,
            text="updated_message",
            type=MessageType.QUESTION.value,
        )
        message = await message_repository.get(messages["message_to_upd"].id)
        assert message
        assert message.text == "updated_message"
        assert message.type == MessageType.QUESTION.value
        assert message.chat_id == messages["chat"].id
        await message_repository.update(
            message,
            text="updated_message_2",
        )
        message = await message_repository.get(messages["message_to_upd"].id)
        assert message
        assert message.text == "updated_message_2"
        assert message.type == MessageType.QUESTION.value
        assert message.chat_id == messages["chat"].id


async def test_delete(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        message = await message_repository.get(messages["message_to_del"].id)
        assert message

        await message_repository.delete(message)
        message = await message_repository.get(messages["message_to_del"].id)
        assert message is None


async def test_all(session):
    async with session:
        message_repository = MessageRepository(session)
        messages = await message_repository.all()
        assert len(messages) >= 1


async def test_count(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        messages_count = await message_repository.count(
            {
                "chat_id": messages["chat"].id,
            }
        )
        assert isinstance(messages_count, int)
        assert messages_count >= 1


async def test_exists_true(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        is_exists = await message_repository.exists({"chat_id": messages["chat"].id})
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        message_repository = MessageRepository(session)
        is_exists = await message_repository.exists({"chat_id": uuid.uuid4()})
        assert is_exists is False


async def test_filter(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        result = await message_repository.filter(filters={"text": {"ilike": "filter"}})
        assert len(result) == 3
        result = await message_repository.filter(
            filters={
                "text": {"ilike": "filter"},
                "type": {"in": [MessageType.ANSWER.value, MessageType.QUESTION.value]},
            }
        )
        assert len(result) == 3
        result = await message_repository.filter(
            filters={
                "text": {"ilike": "filter"},
                "type": {
                    "in": [MessageType.ANSWER.value, MessageType.EVALUATION.value]
                },
            }
        )
        assert len(result) == 2
        result = await message_repository.filter(
            filters={
                "text": {"ilike": "filter"},
                "created_at": {
                    "between": (datetime.date(2024, 9, 2), datetime.date(2024, 9, 4))
                },
                "type": {
                    "in": [MessageType.ANSWER.value, MessageType.EVALUATION.value]
                },
            }
        )
        assert len(result) == 1
        result = await message_repository.filter(
            filters={
                "text": {"ilike": "filter"},
                "created_at": {
                    "between": (datetime.date(2023, 9, 2), datetime.date(2023, 9, 4))
                },
                "type": {
                    "in": [MessageType.ANSWER.value, MessageType.EVALUATION.value]
                },
            }
        )
        assert len(result) == 0
        
        
async def test_get_or_create_created(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        obj, created = await message_repository.get_or_create(
            filters={
                "text": "some text",
            },
            chat_id=messages["chat"].id,
            text="some text",
            type=MessageType.ANSWER.value,
        )
        assert created is True
        
        
async def test_get_or_create_not_created(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        obj, created = await message_repository.get_or_create(
            filters={
                "text": "repository_test_message_message_12",
            },
            chat_id=messages["chat"].id,
            text="repository_test_message_message_12",
        )
        assert created is False
        assert obj.id == messages["message_to_upd2"].id
        
        
async def test_get_or_update_created(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        obj, created = await message_repository.get_or_create(
            filters={
                "text": "some text 2",
            },
            chat_id=messages["chat"].id,
            text="some text 2",
            type=MessageType.ANSWER.value,
        )
        assert created is True
        
        
async def test_get_or_update_not_created(session, messages):
    async with session:
        message_repository = MessageRepository(session)
        obj, created = await message_repository.get_or_create(
            filters={
                "text": "repository_test_message_message_12",
            },
            chat_id=messages["chat"].id,
            text="repository_test_message_message_12",
        )
        assert created is False
        assert obj.id == messages["message_to_upd2"].id
