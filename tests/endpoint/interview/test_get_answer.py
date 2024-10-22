import uuid

import pytest

from apps.v1.interview.repository import ChatRepository, QuestionRepository
from apps.v1.interview.service import AnswerService, EvaluationService, MessageService


@pytest.fixture(scope="session")
async def questions(session, auth_headers):
    async with session:
        chat_repository = ChatRepository(session)
        question_repository = QuestionRepository(session)

        chat = await chat_repository.create(
            user_id=auth_headers.get("user").id,
            title="Test chat",
            config={"technologies": [{"technology": "Python", "complexity": "easy"}]},
        )
        question = await question_repository.create(
            text="question_python_easy_2",
            technology="Python",
            complexity="easy",
        )

        return {
            "chat": chat,
            "question": question,
        }


async def test_get_answer_201(session, client, questions, auth_headers, mocker):
    mock_response = mocker.patch(
        "apps.v1.interview.utils.request.get_evaluation_request"
    )
    response_text = """
    Оценка: 5/10\n
    Оценка ответа на вопрос
    """
    mock_response.return_value = {"choices": [{"message": {"content": response_text}}]}
    response = await client.post(
        f"/api/v1/interview/a/{str(questions['chat'].id)}/",
        headers=auth_headers["auth_headers"],
        json={
            "question_id": str(questions["question"].id),
            "text": "answer text",
        },
    )
    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["question_id"]
    assert response.json()["user_id"]
    assert response.json()["text"]

    async with session:
        answer_service = AnswerService(session)
        message_service = MessageService(session)
        evaluation_service = EvaluationService(session)

        answer = await answer_service.get(response.json()["id"])
        if not answer:
            raise AssertionError("No answer found")
        assert answer.question_id == questions["question"].id
        assert answer.text == "answer text"
        assert answer.score == 5

        message_answer = await message_service.filter(
            {"chat_id": questions["chat"].id, "answer_id": answer.id}
        )
        if not message_answer:
            raise AssertionError("No message found")
        assert message_answer[0].text == "answer text"

        message_eval = await message_service.filter(
            {"chat_id": questions["chat"].id, "evaluation_id": {"not_exact": None}}
        )
        if not message_eval:
            raise AssertionError("No message found")
        assert "Оценка: 5/10" in message_eval[0].text
        assert "Оценка ответа на вопрос" in message_eval[0].text

        evaluation = await evaluation_service.filter({"answer_id": answer.id})
        if not evaluation:
            raise AssertionError("No evaluation found")
        assert "Оценка: 5/10" in evaluation[0].text
        assert "Оценка ответа на вопрос" in evaluation[0].text


async def test_get_answer_403(session, client, questions, auth_headers, mocker):
    mock_response = mocker.patch(
        "apps.v1.interview.utils.request.get_evaluation_request"
    )
    response_text = """
    Оценка: 5/10\n
    Оценка ответа на вопрос
    """
    mock_response.return_value = {"choices": [{"message": {"content": response_text}}]}
    response = await client.post(
        f"/api/v1/interview/a/{str(questions['chat'].id)}/",
        headers=auth_headers["auth_headers3"],
        json={
            "question_id": str(questions["question"].id),
            "text": "answer text",
        },
    )
    assert response.status_code == 403


async def test_get_answer_401(session, client, questions, auth_headers, mocker):
    mock_response = mocker.patch(
        "apps.v1.interview.utils.request.get_evaluation_request"
    )
    response_text = """
    Оценка: 5/10\n
    Оценка ответа на вопрос
    """
    mock_response.return_value = {"choices": [{"message": {"content": response_text}}]}
    response = await client.post(
        f"/api/v1/interview/a/{str(questions['chat'].id)}/",
        # headers=auth_headers["auth_headers3"],
        json={
            "question_id": str(questions["question"].id),
            "text": "answer text",
        },
    )
    assert response.status_code == 401


async def test_get_answer_404(session, client, questions, auth_headers, mocker):
    mock_response = mocker.patch(
        "apps.v1.interview.utils.request.get_evaluation_request"
    )
    response_text = """
    Оценка: 5/10\n
    Оценка ответа на вопрос
    """
    mock_response.return_value = {"choices": [{"message": {"content": response_text}}]}
    response = await client.post(
        f"/api/v1/interview/a/{str(uuid.uuid4())}/",
        headers=auth_headers["auth_headers"],
        json={
            "question_id": str(questions["question"].id),
            "text": "answer text",
        },
    )
    assert response.status_code == 404


async def test_get_answer_422(session, client, questions, auth_headers, mocker):
    mock_response = mocker.patch(
        "apps.v1.interview.utils.request.get_evaluation_request"
    )
    response_text = """
    Оценка: 5/10\n
    Оценка ответа на вопрос
    """
    mock_response.return_value = {"choices": [{"message": {"content": response_text}}]}
    response = await client.post(
        f"/api/v1/interview/a/{str(questions['chat'].id)}/",
        headers=auth_headers["auth_headers"],
        json={
            "question_id": str(questions["question"].id),
            # "text": "answer text",
        },
    )
    assert response.status_code == 422
