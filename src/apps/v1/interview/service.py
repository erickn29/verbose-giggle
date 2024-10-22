import random

from uuid import UUID

from apps.v1.interview.model import Answer, Chat, Question
from apps.v1.interview.repository import (
    AnswerRepository,
    ChatRepository,
    EvaluationRepository,
    MessageRepository,
    QuestionRepository,
)
from apps.v1.interview.schema import (
    AnswerCreateInputSchema,
    AnswerUpdateInputSchema,
    EvaluationInputSchema,
    MessageCreateInputSchema,
    MessageType,
)
from apps.v1.interview.utils import request
from apps.v1.user.model import User
from apps.v1.user.service import UserService
from base.service import BaseService
from core.exceptions import exception
from core.settings import settings
from schemas.user import UserModelSchema
from sqlalchemy.ext.asyncio import AsyncSession


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=ChatRepository)


class QuestionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=QuestionRepository)

    async def get_question(
        self, chat_id: UUID, user_schema: UserModelSchema
    ) -> Question:
        chat_service = ChatService(self.session)
        user_service = UserService(self.session)

        if not isinstance(user_schema.id, UUID):
            user_schema.id = UUID(user_schema.id)
        user: User | None = await user_service.get(user_schema.id)
        chat: Chat | None = await chat_service.get(chat_id)
        if not user or not chat:
            raise exception(404, "Чат или пользователь не найдены")
        user_questions_by_chat = [
            await self.get(m.question_id)
            for m in chat.messages
            if m.question_id is not None
        ]
        # used_question_ids = [answer.question_id for answer in user.answers]
        questions_by_chat_config = await self.filter(
            {
                "technology": {
                    "in": [t.get("technology") for t in chat.config["technologies"]]
                },
                "complexity": {
                    "in": [t.get("complexity") for t in chat.config["technologies"]]
                },
                "id": {"not_in": [q.id for q in user_questions_by_chat]},
            }
        )
        if not questions_by_chat_config:
            questions_by_chat_config = await self.filter(
            {
                "technology": {
                    "in": [t.get("technology") for t in chat.config["technologies"]]
                },
                "complexity": {
                    "in": [t.get("complexity") for t in chat.config["technologies"]]
                },
            }
        )
        question = random.choice(questions_by_chat_config)
        message_service = MessageService(self.session)
        await message_service.create(
            **MessageCreateInputSchema(
                chat_id=chat_id,
                text=question.text,
                type=MessageType.QUESTION.value,
                question_id=question.id,
            ).model_dump()
        )
        return question


class AnswerService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=AnswerRepository)

    async def get_answer(
        self,
        schema: AnswerCreateInputSchema,
        user_schema: UserModelSchema,
        chat_id: UUID,
    ) -> Answer:
        chat_service = ChatService(self.session)
        message_service = MessageService(self.session)
        evaluation_service = EvaluationService(self.session)
        schema.user_id = (
            user_schema.id if isinstance(user_schema.id, UUID) else UUID(user_schema.id)
        )

        chat = await chat_service.get(chat_id)
        if not chat:
            raise exception(404, "Чат не найден")
        answer: Answer = await self.create(**schema.model_dump())
        await message_service.create(
            **MessageCreateInputSchema(
                chat_id=chat.id,
                text=answer.text,
                type=MessageType.ANSWER.value,
                answer_id=answer.id,
            ).model_dump()
        )
        await evaluation_service.get_evaluation(chat, answer)
        return answer


class EvaluationService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=EvaluationRepository)

    async def get_evaluation(self, chat: Chat, answer: Answer):
        message_service = MessageService(self.session)
        technologies = [t.get("technology") for t in chat.config["technologies"]]
        default_text = "Что-то пошло не так, попробуйте позже"
        prompt = f"""
        Ты - опытный разработчик. Ты эксперт в таких технологиях как 
        {''.join(technologies)}. 
        На вход тебе подается вопрос и ответ на него. 
        Очень строго и внимательно проверяй правильность и полноту ответа на вопрос. 
        В ответе дававй оценку ответу пользователя на вопрос. 
        Говори что верно и что неверно сказано. Что можно добавить к ответу на вопрос.
        Формат ответа:
        - оценка от 1 до 10 (например 5/10)
        - что сказано верно
        - что сказано неверно
        - рекомендации
        """
        question = await answer.awaitable_attrs.question
        user_answer = f"""
        Вопрос: {question.text}.
        Ответ: {answer.text}.
        """
        response = await request.get_evaluation_request(
            url=settings.ai.SERVICE_URL,
            data={
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_answer},
                ],
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False,
            },
        )
        if (
            not response
            or not response.get("choices")
            or not response["choices"][0].get("message")
            or not response["choices"][0]["message"].get("content")
        ):
            await message_service.create(
                **MessageCreateInputSchema(
                    chat_id=chat.id,
                    text=default_text,
                    type=MessageType.EVALUATION.value,
                ).model_dump()
            )
            return
        evaluation_text = (
            response["choices"][0]["message"]["content"].strip().replace("\n", "<br>")
        )
        evaluation = await self.create(
            **EvaluationInputSchema(
                answer_id=answer.id, text=evaluation_text
            ).model_dump()
        )
        await message_service.create(
            **MessageCreateInputSchema(
                chat_id=chat.id,
                text=evaluation_text,
                type=MessageType.EVALUATION.value,
                evaluation_id=evaluation.id,
            ).model_dump()
        )
        if "Оценка" in evaluation_text and "/10" in evaluation_text:
            eval_string = evaluation_text.split("/10")[0]
            eval_num = eval_string.split(" ")[-1]
            if eval_num.isdigit():
                answer_service = AnswerService(session=self.session)
                await answer_service.update(
                    answer,
                    **AnswerUpdateInputSchema(score=int(eval_num)).model_dump(),
                )
                return
        return


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=MessageRepository)
