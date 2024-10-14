import datetime

import pytest

from apps.v1.interview.model import Question
from apps.v1.interview.service import (
    AnswerService,
    ChatService,
    QuestionService,
)
from schemas.user import UserModelSchema


@pytest.fixture(scope="session")
async def questions(session, auth_headers):
    chat_service = ChatService(session)
    chat = await chat_service.create(
        user_id=auth_headers["user"].id,
        title=f"chat_{auth_headers["user"].email}",
        config={
            "technologies": [
                {"technology": "php", "complexity": "easy"},
                {"technology": "vue", "complexity": "medium"},
            ]
        },
    )
    question_service = QuestionService(session)
    question_to_upd = await question_service.create(
        text="Question1",
        technology="python3",
        complexity="easy",
    )
    question_to_upd2 = await question_service.create(
        text="Question1212",
        technology="python3",
        complexity="easy",
    )
    question_to_del = await question_service.create(
        technology="python3",
        text="repository_test_question_question_2",
        complexity="easy",
    )
    await question_service.create(
        technology="python3",
        text="repository_test_question_question_ffilter_1",
        complexity="easy",
        created_at=datetime.date(2024, 9, 1),
    )
    await question_service.create(
        technology="react",
        text="repository_test_question_question_ffilter_2",
        complexity="easy",
        created_at=datetime.date(2024, 9, 3),
    )
    await question_service.create(
        technology="python3",
        text="repository_test_question_question_ffilter_3",
        complexity="medium",
        created_at=datetime.date(2024, 9, 5),
    )

    q1 = await question_service.create(
        technology="php",
        text="test_q1",
        complexity="easy",
        created_at=datetime.date(2024, 9, 1),
    )
    q2 = await question_service.create(
        technology="vue",
        text="test_q2",
        complexity="medium",
        created_at=datetime.date(2024, 9, 3),
    )
    q3 = await question_service.create(
        technology="php",
        text="test_q3",
        complexity="easy",
        created_at=datetime.date(2024, 9, 5),
    )
    await question_service.create(
        technology="go",
        text="test_q4",
        complexity="easy",
        created_at=datetime.date(2024, 9, 5),
    )
    await question_service.create(
        technology="angular",
        text="test_q5",
        complexity="easy",
        created_at=datetime.date(2024, 9, 5),
    )

    return {
        "question_to_upd": question_to_upd,
        "question_to_upd2": question_to_upd2,
        "question_to_del": question_to_del,
        "chat": chat,
        "q1": q1,
        "q2": q2,
        "q3": q3,
    }


async def test_get_question(session, questions, auth_headers):
    async with session:
        question_service = QuestionService(session)
        question_1 = await question_service.get_question(
            questions["chat"].id, UserModelSchema.model_validate(auth_headers["user"])
        )
    assert isinstance(question_1, Question)
    assert question_1.id in [questions["q1"].id, questions["q2"].id, questions["q3"].id]

    async with session:
        answer_service = AnswerService(session)
        await answer_service.create(
            text="answer_1",
            score=5,
            question_id=question_1.id,
            user_id=auth_headers["user"].id,
        )
    async with session:
        question_service = QuestionService(session)
        question_2 = await question_service.get_question(
            questions["chat"].id, UserModelSchema.model_validate(auth_headers["user"])
        )
    assert isinstance(question_2, Question)
    assert question_2.id in [questions["q1"].id, questions["q2"].id, questions["q3"].id]

    async with session:
        answer_service = AnswerService(session)
        await answer_service.create(
            text="answer_2",
            score=5,
            question_id=question_2.id,
            user_id=auth_headers["user"].id,
        )

    assert question_1.text != question_2.text

    async with session:
        question_service = QuestionService(session)
        question_3 = await question_service.get_question(
            questions["chat"].id, UserModelSchema.model_validate(auth_headers["user"])
        )
    assert isinstance(question_3, Question)
    assert question_3.id in [questions["q1"].id, questions["q2"].id, questions["q3"].id]

    async with session:
        answer_service = AnswerService(session)
        await answer_service.create(
            text="answer_3",
            score=5,
            question_id=question_3.id,
            user_id=auth_headers["user"].id,
        )

    assert question_1.text != question_2.text != question_3.text

    async with session:
        question_service = QuestionService(session)
        question_4 = await question_service.get_question(
            questions["chat"].id, UserModelSchema.model_validate(auth_headers["user"])
        )
        
    assert isinstance(question_4, Question)
    assert question_4.id == question_1.id
        
    async with session:
        answer_service = AnswerService(session)
        await answer_service.create(
            text="answer_3",
            score=5,
            question_id=question_4.id,
            user_id=auth_headers["user"].id,
        )
    
    async with session:
        question_service = QuestionService(session)
        question_5 = await question_service.get_question(
            questions["chat"].id, UserModelSchema.model_validate(auth_headers["user"])
        )
    assert isinstance(question_5, Question)
    assert question_5.id == question_2.id
    
    async with session:
        answer_service = AnswerService(session)
        await answer_service.create(
            text="answer_3",
            score=5,
            question_id=question_5.id,
            user_id=auth_headers["user"].id,
        )
    
    async with session:
        question_service = QuestionService(session)
        question_6 = await question_service.get_question(
            questions["chat"].id, UserModelSchema.model_validate(auth_headers["user"])
        )
    assert isinstance(question_6, Question)
    assert question_6.id == question_3.id
    
    async with session:
        answer_service = AnswerService(session)
        await answer_service.create(
            text="answer_3",
            score=5,
            question_id=question_6.id,
            user_id=auth_headers["user"].id,
        )


async def test_get(session, questions):
    async with session:
        question_service = QuestionService(session)
        question = await question_service.get(questions["question_to_upd"].id)
        assert isinstance(question, Question)
        assert question.id == questions["question_to_upd"].id


async def test_create(session, questions):
    async with session:
        question_service = QuestionService(session)
        question = await question_service.create(
            technology="python3",
            text="repository_test_question_question_22",
            complexity="hard",
        )
        assert question.id is not None
        assert question.technology == "python3"
        assert question.text == "repository_test_question_question_22"
        assert question.complexity == "hard"

        obj_question = await question_service.get(question.id)
        if not obj_question:
            raise AssertionError("Question not found")

        assert obj_question.technology == "python3"
        assert obj_question.text == "repository_test_question_question_22"
        assert obj_question.complexity == "hard"


async def test_update(session, questions):
    async with session:
        question_service = QuestionService(session)
        question = await question_service.get(questions["question_to_upd"].id)
        assert question
        await question_service.update(
            question,
            text="updated_question",
        )
        question = await question_service.get(questions["question_to_upd"].id)
        assert question
        assert question.text == "updated_question"
        await question_service.update(
            question,
            text="updated_question_2",
        )
        question = await question_service.get(questions["question_to_upd"].id)
        assert question
        assert question.text == "updated_question_2"


async def test_delete(session, questions):
    async with session:
        question_service = QuestionService(session)
        question = await question_service.get(questions["question_to_del"].id)
        assert question

        await question_service.delete(question)
        question = await question_service.get(questions["question_to_del"].id)
        assert question is None


async def test_all(session):
    async with session:
        question_service = QuestionService(session)
        questions = await question_service.all()
        assert len(questions) >= 1


async def test_count(session, questions):
    async with session:
        question_service = QuestionService(session)
        questions_count = await question_service.count(
            {
                "technology": "python3",
            }
        )
        assert isinstance(questions_count, int)
        assert questions_count >= 1


async def test_exists_true(session, questions):
    async with session:
        question_service = QuestionService(session)
        is_exists = await question_service.exists({"technology": "python3"})
        assert is_exists is True


async def test_exists_false(session):
    async with session:
        question_service = QuestionService(session)
        is_exists = await question_service.exists({"technology": "xxx"})
        assert is_exists is False


async def test_filter(session, questions):
    async with session:
        question_service = QuestionService(session)
        result = await question_service.filter(filters={"text": {"ilike": "ffilter"}})
        assert len(result) == 3
        result = await question_service.filter(
            filters={
                "text": {"ilike": "ffilter"},
                "technology": {"in": ["python3", "react"]},
                "complexity": {"in": ["easy", "medium"]},
            }
        )
        assert len(result) == 3
        result = await question_service.filter(
            filters={
                "text": {"ilike": "ffilter"},
                "technology": {"in": ["python3", "react"]},
                "complexity": {"in": ["easy"]},
            }
        )
        assert len(result) == 2
        result = await question_service.filter(
            filters={
                "text": {"ilike": "ffilter"},
                "created_at": {
                    "between": (datetime.date(2024, 9, 2), datetime.date(2024, 9, 4))
                },
                "complexity": {"in": ["easy"]},
            }
        )
        assert len(result) == 1
        result = await question_service.filter(
            filters={
                "text": {"ilike": "ffilter"},
                "created_at": {
                    "between": (datetime.date(2023, 9, 2), datetime.date(2023, 9, 4))
                },
                "complexity": {"in": ["hard"]},
            }
        )
        assert len(result) == 0


async def test_get_or_create_created(session, questions):
    async with session:
        question_service = QuestionService(session)
        obj, created = await question_service.get_or_create(
            filters={
                "text": "some text0",
            },
            technology="sql",
            text="some text0",
            complexity="easy",
        )
        assert created is True


async def test_get_or_create_not_created(session, questions):
    async with session:
        question_service = QuestionService(session)
        obj, created = await question_service.get_or_create(
            filters={
                "text": "Question1212",
            },
            text="Question1212",
        )
        assert created is False
        assert obj.id == questions["question_to_upd2"].id


async def test_get_or_update_created(session, questions):
    async with session:
        question_service = QuestionService(session)
        obj, created = await question_service.get_or_create(
            filters={
                "text": "some text 23",
            },
            technology="sql",
            text="some text 23",
            complexity="medium",
        )
        assert created is True


async def test_get_or_update_not_created(session, questions):
    async with session:
        question_service = QuestionService(session)
        obj, created = await question_service.get_or_create(
            filters={
                "text": "Question1212",
            },
            text="Question1212",
        )
        assert created is False
        assert obj.id == questions["question_to_upd2"].id
