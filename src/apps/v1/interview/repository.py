from apps.v1.interview.model import Answer, Chat, Evaluation, Message, Question
from repository.alchemy_orm import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Chat)


class QuestionRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Question)


class AnswerRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Answer)
        
        
class EvaluationRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Evaluation)


class MessageRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Message)
