from typing import Annotated

from apps.v1.auth.model import RecoveryToken
from base.repository import BaseRepository
from core.database import db_conn

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class RecoveryTokenRepository(BaseRepository):
    model = RecoveryToken

    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_conn.get_session),
        ],
    ) -> None:
        super().__init__(session=session, model=RecoveryToken)
