from typing import Annotated
from uuid import UUID

from requests import session

from apps.v1.auth.utils.auth import is_authenticated
from apps.v1.interview.schema import (
    ChatCreateInputSchema,
    ChatCreateOutputSchema,
    ChatDetailOutputSchema,
    ChatListOutputSchema,
)
from apps.v1.interview.service import ChatService, QuestionService
from apps.v1.user.model import User
from core.database import db_conn
from core.exceptions import exception
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


@router.get("/chat/", status_code=200, response_model=ChatListOutputSchema)
async def get_chats(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[User, Depends(is_authenticated)],
):
    chat_service = ChatService(session)
    return ChatListOutputSchema(
        items=await chat_service.fetch(filters={"user_id": user.id})
    )


@router.get("/chat/{chat_id}/", status_code=200, response_model=ChatDetailOutputSchema)
async def get_chat(
    chat_id: UUID,
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[User, Depends(is_authenticated)],
):
    chat_service = ChatService(session)
    chat = await chat_service.get(chat_id)
    if chat.user_id != user.id:
        raise exception(403, "Доступ запрещен")
    return chat


@router.get("/q/{chat_id}/", status_code=200)
async def send_question(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[User, Depends(is_authenticated)],
    chat_id: UUID,
):
    """Генерирует и отправляет вопрос пользователю"""
    question_service = QuestionService(session)
    return await question_service.get_question(chat_id=chat_id, user=user)


@router.post("/a/")
async def get_answer():
    """Принимает ответ от пользователя и дает оценку"""
    return {"status": "ok"}
