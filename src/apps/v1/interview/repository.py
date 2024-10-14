from uuid import UUID

from apps.v1.interview.model import Answer, Chat, Evaluation, Message, Question
from base.repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository(BaseRepository):
    model = Chat

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


class QuestionRepository(BaseRepository):
    model = Question

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


class AnswerRepository(BaseRepository):
    model = Answer

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


class EvaluationRepository(BaseRepository):
    model = Evaluation

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


class MessageRepository(BaseRepository):
    model = Message

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
