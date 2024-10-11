import uuid

import pytest

from apps.v1.interview.model import Answer, Evaluation
from apps.v1.interview.repository import (
    AnswerRepository,
    EvaluationRepository,
    QuestionRepository,
)
from apps.v1.user.repository import UserRepository


@pytest.fixture(scope="session")
async def evaluations(session):
    user_repository = UserRepository(session)
    question_repository = QuestionRepository(session)
    answer_repository = AnswerRepository(session)
    evaluation_repository = EvaluationRepository(session)

    user = await user_repository.create(
        email="user@evaluation.com",
        password="user@user.com",
    )
    question = await question_repository.create(
        text="Question1",
        technology="rust",
        complexity="easy",
    )
    answer = await answer_repository.create(
        user_id=user.id,
        question_id=question.id,
        score=5,
        text="repository_test_evaluation_evaluation_0",
        complexity="hard",
        technology="rust",
    )

    evaluation_to_upd = await evaluation_repository.create(
        answer_id=answer.id,
        text="repository_test_answer_answer_1",
    )
    evaluation_to_del = await evaluation_repository.create(
        answer_id=answer.id,
        text="repository_test_answer_answer_2",
    )

    return {
        "user": user,
        "answer": answer,
        "evaluation_to_upd": evaluation_to_upd,
        "evaluation_to_del": evaluation_to_del,
    }


async def test_get(session, evaluations):
    async with session:
        evaluation_repository = EvaluationRepository(session)
        evaluation = await evaluation_repository.get(evaluations["evaluation_to_upd"].id)
        assert isinstance(evaluation, Evaluation)
        assert evaluation.id == evaluations["evaluation_to_upd"].id


async def test_create(session, evaluations):
    async with session:
        answer_repository = AnswerRepository(session)
        answer = await answer_repository.create(
            user_id=evaluations["user"].id,
            question_id=evaluations["question"].id,
            score=5,
            text="repository_test_answer_answer_3",
        )
        assert answer.id is not None
        assert answer.user_id == evaluations["user"].id
        assert answer.question_id == evaluations["question"].id
        assert answer.text == "repository_test_answer_answer_3"
        assert answer.score == 5

        obj_answer = await answer_repository.get(answer.id)
        if not obj_answer:
            raise AssertionError("Answer not found")

        assert obj_answer.id is not None
        assert obj_answer.user_id == evaluations["user"].id
        assert obj_answer.question_id == evaluations["question"].id
        assert obj_answer.text == "repository_test_answer_answer_3"
        assert obj_answer.score == 5


async def test_update(session, evaluations):
    async with session:
        answer_repository = AnswerRepository(session)
        answer = await answer_repository.get(evaluations["answer_to_upd"].id)
        assert answer
        await answer_repository.update(
            answer,
            text="updated_answer",
        )
        answer = await answer_repository.get(evaluations["answer_to_upd"].id)
        assert answer
        assert answer.text == "updated_answer"
        assert answer.user_id == evaluations["user"].id


async def test_delete(session, evaluations):
    async with session:
        answer_repository = AnswerRepository(session)
        answer = await answer_repository.get(evaluations["answer_to_del"].id)
        assert answer

        await answer_repository.delete(answer)
        answer = await answer_repository.get(evaluations["answer_to_del"].id)
        assert answer is None


async def test_all(session, evaluations):
    async with session:
        answer_repository = AnswerRepository(session)
        evaluations = await answer_repository.all()
        assert len(evaluations) >= 1


async def test_count(session, evaluations):
    async with session:
        answer_repository = AnswerRepository(session)
        chats_count = await answer_repository.count(
            {
                "user_id": evaluations["user"].id,
            }
        )
        assert isinstance(chats_count, int)
        assert chats_count >= 1


async def test_exists_true(session, evaluations):
    async with session:
        answer_repository = AnswerRepository(session)
        is_exists = await answer_repository.exists({"user_id": evaluations["user"].id})
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        answer_repository = AnswerRepository(session)
        is_exists = await answer_repository.exists({"user_id": uuid.uuid4()})
        assert is_exists is False
