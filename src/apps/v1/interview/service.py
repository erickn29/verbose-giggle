from apps.v1.interview.repository import (
    AnswerRepository,
    ChatRepository,
    MessageRepository,
    QuestionRepository,
)
from base.service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=ChatRepository)


class QuestionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=QuestionRepository)


class AnswerService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=AnswerRepository)


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=MessageRepository)
