from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from v1.user.schema.schema import UserOutputSchema, UserCreateSchema, \
    UserListOutputSchema
from v1.user.service.service import UserService


router = APIRouter()


@router.get("/", response_model=UserListOutputSchema)
async def user_list(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    user_service = UserService(session)
    return await user_service.all()


@router.post('/', response_model=UserOutputSchema)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: Annotated[UserCreateSchema, Body(...)]
):
    user_service = UserService(session)
    return await user_service.create(data)
