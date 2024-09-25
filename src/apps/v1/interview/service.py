import random

from uuid import UUID

from apps.v1.interview.model import Answer
from apps.v1.interview.repository import (
    AnswerRepository,
    ChatRepository,
    MessageRepository,
    QuestionRepository,
)
from apps.v1.interview.schema import (
    AnswerCreateInputSchema,
    AnswerUpdateInputSchema,
    MessageCreateInputSchema,
)
from apps.v1.interview.utils.request import get_evaluation
from apps.v1.user.model import User
from base.service import BaseService
from core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=ChatRepository)


class QuestionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=QuestionRepository)

    async def get_question(self, chat_id: UUID, user: User) -> str:
        chat_service = ChatService(self.session)
        question_service = QuestionService(self.session)

        chat = await chat_service.get(chat_id)
        used_question_ids = [answer.question_id for answer in user.answers]
        questions_by_chat_config = await question_service.fetch(
            {
                "technology": {
                    "in": [t.get("technology") for t in chat.config["technologies"]]
                },
                "complexity": {
                    "in": [t.get("complexity") for t in chat.config["technologies"]]
                },
                "id": {"not_in": used_question_ids},
            }
        )
        if not questions_by_chat_config:
            return "Все вопросы кончились =("
        question = random.choice(questions_by_chat_config)
        message_service = MessageService(self.session)
        await message_service.create(
            MessageCreateInputSchema(
                chat_id=chat_id,
                text=question.text,
                is_user_message=False,
            )
        )
        return question


class AnswerService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=AnswerRepository)

    async def get_evaluation(
        self,
        schema: AnswerCreateInputSchema,
        user: User,
        chat_id: UUID,
    ) -> Answer:
        chat_service = ChatService(self.session)
        message_service = MessageService(self.session)
        schema.user_id = user.id

        chat = await chat_service.get(chat_id)
        answer = await self.create(schema)
        await message_service.create(
            MessageCreateInputSchema(
                chat_id=chat.id,
                text=answer.text,
                is_user_message=True,
            )
        )
        technologies = [t.get("technology") for t in chat.config["technologies"]]
        prompt = f"""
        Ты - опытный разработчик. Ты эксперт в таких технологиях как 
        {''.join(technologies)}. Ты проводишь собеседование и тебе нужно очень
        тщательно выбрать кандидатов. Очень строго и внимательно проверяй то что я 
        ввожу. В ответе дававй оценку тому, что ввел пользователь. Говори что верно 
        и что неверно сказано.
        Формат ответа:
        - оценка от 1 до 10
        - что сказано верно
        - что сказано неверно
        - рекомендации
        """
        response = await get_evaluation(
            url=settings.ai.SERVICE_URL,
            data={
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": answer.text},
                ],
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False,
            },
        )
        if (
            response
            and response.get("choices")
            and response["choices"][0].get("message")
            and response["choices"][0]["message"].get("content")
        ):
            evaluation = response["choices"][0]["message"]["content"].strip()
            await message_service.create(
                MessageCreateInputSchema(
                    chat_id=chat.id,
                    text=evaluation,
                    is_user_message=False,
                )
            )
            if "Оценка: " in evaluation and "/10" in evaluation:
                eval_string = evaluation.split("/10")[0]
                eval_num = eval_string.split(" ")[-1]
                if eval_num.isdigit():
                    await self.update(
                        answer.id, AnswerUpdateInputSchema(score=int(eval_num))
                    )
            return answer


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=MessageRepository)
