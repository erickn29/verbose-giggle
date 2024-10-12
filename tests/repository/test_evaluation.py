import uuid

import pytest

from apps.v1.interview.model import Evaluation
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
    )

    evaluation_to_upd = await evaluation_repository.create(
        answer_id=answer.id,
        text="repository_test_evaluation_evaluation_1",
    )
    evaluation_to_del = await evaluation_repository.create(
        answer_id=answer.id,
        text="repository_test_evaluation_evaluation_2",
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
        evaluation = await evaluation_repository.get(
            evaluations["evaluation_to_upd"].id
        )
        assert isinstance(evaluation, Evaluation)
        assert evaluation.id == evaluations["evaluation_to_upd"].id


async def test_create(session, evaluations):
    async with session:
        evaluation_repository = EvaluationRepository(session)
        evaluation = await evaluation_repository.create(
            answer_id=evaluations["answer"].id,
            text="repository_test_evaluation_evaluation_1",
        )
        assert evaluation.id is not None
        assert evaluation.answer_id == evaluations["answer"].id
        assert evaluation.text == "repository_test_evaluation_evaluation_1"

        obj_evaluation = await evaluation_repository.get(evaluation.id)
        if not obj_evaluation:
            raise AssertionError("Answer not found")

        assert obj_evaluation.id is not None
        assert obj_evaluation.answer_id == evaluations["answer"].id
        assert obj_evaluation.text == "repository_test_evaluation_evaluation_1"


async def test_exists_true(session, evaluations):
    async with session:
        evaluation_repository = EvaluationRepository(session)
        is_exists = await evaluation_repository.exists(
            {"answer_id": evaluations["answer"].id}
        )
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        evaluation_repository = EvaluationRepository(session)
        is_exists = await evaluation_repository.exists({"answer_id": uuid.uuid4()})
        assert is_exists is False
