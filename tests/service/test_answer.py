import uuid

import pytest

from apps.v1.interview.model import Answer
from apps.v1.interview.service import AnswerService, QuestionService
from apps.v1.user.service import UserService


@pytest.fixture(scope="session")
async def answers(session):
    user_service = UserService(session)
    question_service = QuestionService(session)
    answer_service = AnswerService(session)

    user = await user_service.create(
        email="user@answer_service.com",
        password="user@user.com",
    )
    question = await question_service.create(
        text="Question1",
        technology="rust",
        complexity="easy",
    )

    answer_to_upd = await answer_service.create(
        user_id=user.id,
        question_id=question.id,
        score=5,
        text="service_test_answer_answer_1",
    )
    answer_to_del = await answer_service.create(
        user_id=user.id,
        question_id=question.id,
        score=5,
        text="service_test_answer_answer_2",
    )

    return {
        "user": user,
        "question": question,
        "answer_to_upd": answer_to_upd,
        "answer_to_del": answer_to_del,
    }


async def test_get(session, answers):
    async with session:
        answer_service = AnswerService(session)
        answer = await answer_service.get(answers["answer_to_upd"].id)
        assert isinstance(answer, Answer)
        assert answer.id == answers["answer_to_upd"].id


async def test_create(session, answers):
    async with session:
        answer_service = AnswerService(session)
        answer = await answer_service.create(
            user_id=answers["user"].id,
            question_id=answers["question"].id,
            score=5,
            text="service_test_answer_answer_3",
        )
        assert answer.id is not None
        assert answer.user_id == answers["user"].id
        assert answer.question_id == answers["question"].id
        assert answer.text == "service_test_answer_answer_3"
        assert answer.score == 5

        obj_answer = await answer_service.get(answer.id)
        if not obj_answer:
            raise AssertionError("Answer not found")

        assert obj_answer.id is not None
        assert obj_answer.user_id == answers["user"].id
        assert obj_answer.question_id == answers["question"].id
        assert obj_answer.text == "service_test_answer_answer_3"
        assert obj_answer.score == 5


async def test_update(session, answers):
    async with session:
        answer_service = AnswerService(session)
        answer = await answer_service.get(answers["answer_to_upd"].id)
        assert answer
        await answer_service.update(
            answer,
            text="updated_answer",
        )
        answer = await answer_service.get(answers["answer_to_upd"].id)
        assert answer
        assert answer.text == "updated_answer"
        assert answer.user_id == answers["user"].id


async def test_delete(session, answers):
    async with session:
        answer_service = AnswerService(session)
        answer = await answer_service.get(answers["answer_to_del"].id)
        assert answer

        await answer_service.delete(answer)
        answer = await answer_service.get(answers["answer_to_del"].id)
        assert answer is None


async def test_all(session, answers):
    async with session:
        answer_service = AnswerService(session)
        answers = await answer_service.all()
        assert len(answers) >= 1


async def test_count(session, answers):
    async with session:
        answer_service = AnswerService(session)
        chats_count = await answer_service.count(
            {
                "user_id": answers["user"].id,
            }
        )
        assert isinstance(chats_count, int)
        assert chats_count >= 1


async def test_exists_true(session, answers):
    async with session:
        answer_service = AnswerService(session)
        is_exists = await answer_service.exists({"user_id": answers["user"].id})
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        answer_service = AnswerService(session)
        is_exists = await answer_service.exists({"user_id": uuid.uuid4()})
        assert is_exists is False
