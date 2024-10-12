import datetime
import uuid

import pytest

from apps.v1.interview.model import Message
from apps.v1.interview.schema import MessageType
from apps.v1.interview.service import ChatService, MessageService
from apps.v1.user.service import UserService


@pytest.fixture(scope="session")
async def messages(session):
    user_service = UserService(session)
    chat_service = ChatService(session)
    message_service = MessageService(session)

    user = await user_service.create(
        email="user@message_service.com",
        password="user@user.com",
    )
    chat = await chat_service.create(
        user_id=user.id,
        title="service_test_message_chat_1",
        config={},
    )
    message_to_upd = await message_service.create(
        chat_id=chat.id,
        text="service_test_message_message_1",
        type=MessageType.ANSWER.value,
    )
    message_to_upd2 = await message_service.create(
        chat_id=chat.id,
        text="service_test_message_message_12",
        type=MessageType.ANSWER.value,
    )
    message_to_del = await message_service.create(
        chat_id=chat.id,
        text="service_test_message_message_2",
        type=MessageType.ANSWER.value,
    )
    await message_service.create(
        chat_id=chat.id,
        text="service_test_message_message_filterr_1",
        type=MessageType.ANSWER.value,
        created_at=datetime.date(2024, 9, 1),
    )
    await message_service.create(
        chat_id=chat.id,
        text="service_test_message_message_filterr_2",
        type=MessageType.ANSWER.value,
        created_at=datetime.date(2024, 9, 3),
    )
    await message_service.create(
        chat_id=chat.id,
        text="service_test_message_message_filterr_3",
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
        message_service = MessageService(session)
        message = await message_service.get(messages["message_to_upd"].id)
        assert isinstance(message, Message)
        assert message.id == messages["message_to_upd"].id


async def test_create(session, messages):
    async with session:
        message_service = MessageService(session)
        message = await message_service.create(
            chat_id=messages["chat"].id,
            text="test_message",
            type=MessageType.EVALUATION.value,
        )
        assert message.id is not None
        assert message.chat_id == messages["chat"].id
        assert message.text == "test_message"
        assert message.type == MessageType.EVALUATION.value

        obj_message = await message_service.get(message.id)
        if not obj_message:
            raise AssertionError("Message not found")

        assert obj_message.chat_id == messages["chat"].id
        assert obj_message.text == "test_message"
        assert obj_message.type == MessageType.EVALUATION.value


async def test_update(session, messages):
    async with session:
        message_service = MessageService(session)
        message = await message_service.get(messages["message_to_upd"].id)
        assert message
        await message_service.update(
            message,
            text="updated_message",
            type=MessageType.QUESTION.value,
        )
        message = await message_service.get(messages["message_to_upd"].id)
        assert message
        assert message.text == "updated_message"
        assert message.type == MessageType.QUESTION.value
        assert message.chat_id == messages["chat"].id
        await message_service.update(
            message,
            text="updated_message_2",
        )
        message = await message_service.get(messages["message_to_upd"].id)
        assert message
        assert message.text == "updated_message_2"
        assert message.type == MessageType.QUESTION.value
        assert message.chat_id == messages["chat"].id


async def test_delete(session, messages):
    async with session:
        message_service = MessageService(session)
        message = await message_service.get(messages["message_to_del"].id)
        assert message

        await message_service.delete(message)
        message = await message_service.get(messages["message_to_del"].id)
        assert message is None


async def test_all(session):
    async with session:
        message_service = MessageService(session)
        messages = await message_service.all()
        assert len(messages) >= 1


async def test_count(session, messages):
    async with session:
        message_service = MessageService(session)
        messages_count = await message_service.count(
            {
                "chat_id": messages["chat"].id,
            }
        )
        assert isinstance(messages_count, int)
        assert messages_count >= 1


async def test_exists_true(session, messages):
    async with session:
        message_service = MessageService(session)
        is_exists = await message_service.exists({"chat_id": messages["chat"].id})
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        message_service = MessageService(session)
        is_exists = await message_service.exists({"chat_id": uuid.uuid4()})
        assert is_exists is False


async def test_filter(session, messages):
    async with session:
        message_service = MessageService(session)
        result = await message_service.filter(filters={"text": {"ilike": "filterr"}})
        assert len(result) == 3
        result = await message_service.filter(
            filters={
                "text": {"ilike": "filterr"},
                "type": {"in": [MessageType.ANSWER.value, MessageType.QUESTION.value]},
            }
        )
        assert len(result) == 3
        result = await message_service.filter(
            filters={
                "text": {"ilike": "filterr"},
                "type": {
                    "in": [MessageType.ANSWER.value, MessageType.EVALUATION.value]
                },
            }
        )
        assert len(result) == 2
        result = await message_service.filter(
            filters={
                "text": {"ilike": "filterr"},
                "created_at": {
                    "between": (datetime.date(2024, 9, 2), datetime.date(2024, 9, 4))
                },
                "type": {
                    "in": [MessageType.ANSWER.value, MessageType.EVALUATION.value]
                },
            }
        )
        assert len(result) == 1
        result = await message_service.filter(
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
        message_service = MessageService(session)
        obj, created = await message_service.get_or_create(
            filters={
                "text": "some text2",
            },
            chat_id=messages["chat"].id,
            text="some text2",
            type=MessageType.ANSWER.value,
        )
        assert created is True


async def test_get_or_create_not_created(session, messages):
    async with session:
        message_service = MessageService(session)
        obj, created = await message_service.get_or_create(
            filters={
                "text": "service_test_message_message_12",
            },
            chat_id=messages["chat"].id,
            text="service_test_message_message_12",
        )
        assert created is False
        assert obj.id == messages["message_to_upd2"].id


async def test_get_or_update_created(session, messages):
    async with session:
        message_service = MessageService(session)
        obj, created = await message_service.get_or_create(
            filters={
                "text": "some text 22",
            },
            chat_id=messages["chat"].id,
            text="some text 22",
            type=MessageType.ANSWER.value,
        )
        assert created is True


async def test_get_or_update_not_created(session, messages):
    async with session:
        message_service = MessageService(session)
        obj, created = await message_service.get_or_create(
            filters={
                "text": "service_test_message_message_12",
            },
            chat_id=messages["chat"].id,
            text="service_test_message_message_12",
        )
        assert created is False
        assert obj.id == messages["message_to_upd2"].id
