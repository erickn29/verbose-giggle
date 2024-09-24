import random

from uuid import UUID

from apps.v1.interview.repository import (
    AnswerRepository,
    ChatRepository,
    MessageRepository,
    QuestionRepository,
)
from apps.v1.interview.schema import MessageCreateInputSchema
from apps.v1.user.model import User
from base.service import BaseService
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


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=MessageRepository)
