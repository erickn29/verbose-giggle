import datetime
import uuid

import pytest

from apps.v1.interview.model import Question
from apps.v1.interview.repository import (
    QuestionRepository,
)
from apps.v1.interview.schema import MessageType


@pytest.fixture(scope="session")
async def questions(session):
    question_repository = QuestionRepository(session)
    question_to_upd = await question_repository.create(
        text="Question1",
        technology="python",
        complexity="easy",
    )
    question_to_upd2 = await question_repository.create(
        text="Question12",
        technology="python",
        complexity="easy",
    )
    question_to_del = await question_repository.create(
        technology="python",
        text="repository_test_question_question_2",
        complexity="easy",
    )
    await question_repository.create(
        technology="python",
        text="repository_test_question_question_filter_1",
        complexity="easy",
        created_at=datetime.date(2024, 9, 1),
    )
    await question_repository.create(
        technology="js",
        text="repository_test_question_question_filter_2",
        complexity="easy",
        created_at=datetime.date(2024, 9, 3),
    )
    await question_repository.create(
        technology="python",
        text="repository_test_question_question_filter_3",
        complexity="medium",
        created_at=datetime.date(2024, 9, 5),
    )

    return {
        "question_to_upd": question_to_upd,
        "question_to_upd2": question_to_upd2,
        "question_to_del": question_to_del,
    }


async def test_get(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        question = await question_repository.get(questions["question_to_upd"].id)
        assert isinstance(question, Question)
        assert question.id == questions["question_to_upd"].id


async def test_create(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        question = await question_repository.create(
            technology="python",
            text="repository_test_question_question_22",
            complexity="hard",
        )
        assert question.id is not None
        assert question.technology == "python"
        assert question.text == "repository_test_question_question_22"
        assert question.complexity == "hard"

        obj_question = await question_repository.get(question.id)
        if not obj_question:
            raise AssertionError("Question not found")

        assert obj_question.technology == "python"
        assert obj_question.text == "repository_test_question_question_22"
        assert obj_question.complexity == "hard"


async def test_update(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        question = await question_repository.get(questions["question_to_upd"].id)
        assert question
        await question_repository.update(
            question,
            text="updated_question",
            type=MessageType.QUESTION.value,
        )
        question = await question_repository.get(questions["question_to_upd"].id)
        assert question
        assert question.text == "updated_question"
        assert question.type == MessageType.QUESTION.value
        assert question.chat_id == questions["chat"].id
        await question_repository.update(
            question,
            text="updated_question_2",
        )
        question = await question_repository.get(questions["question_to_upd"].id)
        assert question
        assert question.text == "updated_question_2"
        assert question.type == MessageType.QUESTION.value
        assert question.chat_id == questions["chat"].id


async def test_delete(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        question = await question_repository.get(questions["question_to_del"].id)
        assert question

        await question_repository.delete(question)
        question = await question_repository.get(questions["question_to_del"].id)
        assert question is None


async def test_all(session):
    async with session:
        question_repository = QuestionRepository(session)
        questions = await question_repository.all()
        assert len(questions) >= 1


async def test_count(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        questions_count = await question_repository.count(
            {
                "chat_id": questions["chat"].id,
            }
        )
        assert isinstance(questions_count, int)
        assert questions_count >= 1


async def test_exists_true(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        is_exists = await question_repository.exists({"chat_id": questions["chat"].id})
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        question_repository = QuestionRepository(session)
        is_exists = await question_repository.exists({"chat_id": uuid.uuid4()})
        assert is_exists is False


async def test_filter(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        result = await question_repository.filter(filters={"text": {"ilike": "filter"}})
        assert len(result) == 3
        result = await question_repository.filter(
            filters={
                "text": {"ilike": "filter"},
                "type": {"in": [MessageType.ANSWER.value, MessageType.QUESTION.value]},
            }
        )
        assert len(result) == 3
        result = await question_repository.filter(
            filters={
                "text": {"ilike": "filter"},
                "type": {
                    "in": [MessageType.ANSWER.value, MessageType.EVALUATION.value]
                },
            }
        )
        assert len(result) == 2
        result = await question_repository.filter(
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
        result = await question_repository.filter(
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


async def test_get_or_create_created(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        obj, created = await question_repository.get_or_create(
            filters={
                "text": "some text",
            },
            chat_id=questions["chat"].id,
            text="some text",
            type=MessageType.ANSWER.value,
        )
        assert created is True


async def test_get_or_create_not_created(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        obj, created = await question_repository.get_or_create(
            filters={
                "text": "repository_test_question_question_12",
            },
            chat_id=questions["chat"].id,
            text="repository_test_question_question_12",
        )
        assert created is False
        assert obj.id == questions["question_to_upd2"].id


async def test_get_or_update_created(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        obj, created = await question_repository.get_or_create(
            filters={
                "text": "some text 2",
            },
            chat_id=questions["chat"].id,
            text="some text 2",
            type=MessageType.ANSWER.value,
        )
        assert created is True


async def test_get_or_update_not_created(session, questions):
    async with session:
        question_repository = QuestionRepository(session)
        obj, created = await question_repository.get_or_create(
            filters={
                "text": "repository_test_question_question_12",
            },
            chat_id=questions["chat"].id,
            text="repository_test_question_question_12",
        )
        assert created is False
        assert obj.id == questions["question_to_upd2"].id
