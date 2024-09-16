from apps.v1.user.model import User
from base.repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository):
    model = User

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(session=session, model=User)
