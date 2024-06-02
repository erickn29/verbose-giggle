from typing import Annotated

from core.database import get_async_session
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from v1.vacancy.schema.schema import (
    VacancyCreateSchema,
    VacancyListOutputSchema,
    VacancyOutputSchema,
)
from v1.vacancy.service.service import VacancyService


router = APIRouter()


@router.get("/", response_model=VacancyListOutputSchema)
async def vacancy_list(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.all()


@router.post("/", response_model=VacancyOutputSchema)
async def create_vacancy(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: Annotated[VacancyCreateSchema, Body(...)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.create(data)
