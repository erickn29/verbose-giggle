from typing import Annotated

from apps.v1.auth.utils.auth import is_authenticated
from apps.v1.interview.schema import ChatCreateInputSchema, ChatCreateOutputSchema
from apps.v1.interview.service import ChatService
from apps.v1.user.model import User
from core.database import db_conn
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/chat/", response_model=ChatCreateOutputSchema, status_code=201)
async def create_chat(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[User, Depends(is_authenticated)],
    schema: ChatCreateInputSchema,
):
    """Создает чат с новым пользователем"""
    chat_service = ChatService(session)
    schema.user_id = user.id
    return await chat_service.create(schema)


@router.post("/q/")
async def send_question():
    """Генерирует и отправляет вопрос пользователю"""
    return {"status": "ok"}


@router.post("/a/")
async def get_answer():
    """Принимает ответ от пользователя и дает оценку"""
    return {"status": "ok"}
