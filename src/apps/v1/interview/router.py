from typing import Annotated
from uuid import UUID

from apps.v1.auth.utils.auth import is_verified_email
from apps.v1.interview.schema import (
    AnswerCreateInputSchema,
    AnswerCreateOutputSchema,
    ChatCreateInputSchema,
    ChatCreateOutputSchema,
    ChatDetailOutputSchema,
    ChatListOutputSchema,
    QuestionOutputSchema,
)
from apps.v1.interview.service import (
    AnswerService,
    ChatService,
    QuestionService,
)
from core.database import db_conn
from core.exceptions import exception
from fastapi import APIRouter, Depends, Response
from schemas.user import UserModelSchema
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/chat/", status_code=201)
async def create_chat(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[UserModelSchema, Depends(is_verified_email)],
    schema: ChatCreateInputSchema,
):
    """Создает чат с новым пользователем"""
    chat_service = ChatService(session)
    schema.user_id = user.id if isinstance(user.id, UUID) else UUID(user.id)
    await chat_service.create(**schema.model_dump())
    return Response(status_code=201)


@router.get("/chat/", status_code=200, response_model=ChatListOutputSchema)
async def get_chats(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[UserModelSchema, Depends(is_verified_email)],
):
    chat_service = ChatService(session)
    return ChatListOutputSchema(
        items=[
            ChatCreateOutputSchema.model_validate(chat)
            for chat in await chat_service.filter(filters={"user_id": user.id})
        ]
    )


@router.get("/chat/{chat_id}/", status_code=200, response_model=ChatDetailOutputSchema)
async def get_chat(
    chat_id: UUID,
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[UserModelSchema, Depends(is_verified_email)],
):
    chat_service = ChatService(session)
    chat = await chat_service.get(chat_id)
    if not chat:
        raise exception(404, "Чат не найден")
    user_id = user.id if isinstance(user.id, UUID) else UUID(user.id)
    if chat.user_id != user_id:
        raise exception(403, "Доступ запрещен")
    return chat


@router.get("/q/{chat_id}/", status_code=200, response_model=QuestionOutputSchema)
async def send_question(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[UserModelSchema, Depends(is_verified_email)],
    chat_id: UUID,
):
    """Генерирует и отправляет вопрос пользователю"""
    question_service = QuestionService(session)
    question = await question_service.get_question(chat_id=chat_id, user_schema=user)
    return question


@router.post("/a/{chat_id}/", status_code=201, response_model=AnswerCreateOutputSchema)
async def get_answer(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[UserModelSchema, Depends(is_verified_email)],
    chat_id: UUID,
    schema: AnswerCreateInputSchema,
):
    """Принимает ответ от пользователя и дает оценку"""
    answer_service = AnswerService(session)
    return await answer_service.get_answer(schema, user, chat_id)
