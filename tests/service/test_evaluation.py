import uuid

import pytest

from apps.v1.interview.model import Evaluation
from apps.v1.interview.service import (
    AnswerService,
    EvaluationService,
    QuestionService,
)
from apps.v1.user.service import UserService


@pytest.fixture(scope="session")
async def evaluations(session):
    user_service = UserService(session)
    question_service = QuestionService(session)
    answer_service = AnswerService(session)
    evaluation_service = EvaluationService(session)

    user = await user_service.create(
        email="user@evaluation_service.com",
        password="user@user.com",
    )
    question = await question_service.create(
        text="Question1",
        technology="rust",
        complexity="easy",
    )
    answer = await answer_service.create(
        user_id=user.id,
        question_id=question.id,
        score=5,
        text="repository_test_evaluation_evaluation_0",
    )

    evaluation_to_upd = await evaluation_service.create(
        answer_id=answer.id,
        text="repository_test_evaluation_evaluation_1",
    )
    evaluation_to_del = await evaluation_service.create(
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
        evaluation_service = EvaluationService(session)
        evaluation = await evaluation_service.get(evaluations["evaluation_to_upd"].id)
        assert isinstance(evaluation, Evaluation)
        assert evaluation.id == evaluations["evaluation_to_upd"].id


async def test_create(session, evaluations):
    async with session:
        evaluation_service = EvaluationService(session)
        evaluation = await evaluation_service.create(
            answer_id=evaluations["answer"].id,
            text="repository_test_evaluation_evaluation_1",
        )
        assert evaluation.id is not None
        assert evaluation.answer_id == evaluations["answer"].id
        assert evaluation.text == "repository_test_evaluation_evaluation_1"

        obj_evaluation = await evaluation_service.get(evaluation.id)
        if not obj_evaluation:
            raise AssertionError("Answer not found")

        assert obj_evaluation.id is not None
        assert obj_evaluation.answer_id == evaluations["answer"].id
        assert obj_evaluation.text == "repository_test_evaluation_evaluation_1"


async def test_exists_true(session, evaluations):
    async with session:
        evaluation_service = EvaluationService(session)
        is_exists = await evaluation_service.exists(
            {"answer_id": evaluations["answer"].id}
        )
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        evaluation_service = EvaluationService(session)
        is_exists = await evaluation_service.exists({"answer_id": uuid.uuid4()})
        assert is_exists is False
