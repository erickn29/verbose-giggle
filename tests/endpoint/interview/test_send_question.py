import uuid

import pytest

from apps.v1.interview.repository import ChatRepository, QuestionRepository


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
            text="question_python_easy",
            technology="Python",
            complexity="easy",
        )

        return {
            "chat": chat,
            "question": question,
        }


async def test_send_question_200(client, questions, auth_headers):
    response = await client.get(
        f"/api/v1/interview/q/{str(questions['chat'].id)}/",
        headers=auth_headers["auth_headers"],
    )
    assert response.status_code == 200
    assert response.json()["id"]
    assert response.json()["text"]
    assert response.json()["technology"]
    assert response.json()["complexity"]


async def test_send_question_404(client, questions, auth_headers):
    response = await client.get(
        f"/api/v1/interview/q/{str(uuid.uuid4())}/",
        headers=auth_headers["auth_headers"],
    )
    assert response.status_code == 404


async def test_send_question_401_unauthorized(client, questions, auth_headers):
    response = await client.get(
        f"/api/v1/interview/q/{str(questions['chat'].id)}/",
        # headers=auth_headers["auth_headers"],
    )
    assert response.status_code == 401


async def test_send_question_403_unverified(client, questions, auth_headers):
    response = await client.get(
        f"/api/v1/interview/q/{str(questions['chat'].id)}/",
        headers=auth_headers["auth_headers3"],
    )
    assert response.status_code == 403
