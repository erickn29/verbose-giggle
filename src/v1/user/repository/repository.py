from sqlalchemy.ext.asyncio import AsyncSession

from repository.alchemy_orm import SQLAlchemyRepository
from v1.user.model.model import User


class UserRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)
