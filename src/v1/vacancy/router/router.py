from typing import Annotated
from uuid import UUID

from core.database import get_async_session
from fastapi import APIRouter, Body, Depends, Path
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
    page: int = 1,
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.all(pagination={"current_page": page, "limit": 20})


@router.get("/{vacancy_id}/", response_model=VacancyOutputSchema)
async def vacancy_detail(
    vacancy_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.get_schema(vacancy_id)


@router.post("/", response_model=VacancyOutputSchema, status_code=201)
async def create_vacancy(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: Annotated[VacancyCreateSchema, Body(...)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.create(data)


@router.put("/{vacancy_id}/", response_model=VacancyOutputSchema, status_code=201)
async def update_vacancy(
    vacancy_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: Annotated[VacancyCreateSchema, Body(...)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.update(vacancy_id, data)


@router.delete("/{vacancy_id}/", status_code=204)
async def delete_vacancy(
    vacancy_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.delete(vacancy_id)
