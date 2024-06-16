from typing import Annotated
from uuid import UUID

from starlette.requests import Request
from starlette.responses import JSONResponse

from core.database import get_async_session
from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from v1.vacancy.model.model import Language, Experience, Speciality
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
    request: Request,
    page: int = 1,
):
    vacancy_service = VacancyService(session)
    filters = {}
    params = request.query_params.items()
    for key, value in params:
        if key != "page" and value:
            filters[key] = value
    return await vacancy_service.all(
        pagination={"current_page": page, "limit": 20},
        filters=filters,
    )


@router.get("/selectors/")
async def vacancy_language():
    languages = [lang.value for lang in Language]
    experiences = [exp.value for exp in Experience]
    specialities = [spec.value for spec in Speciality]
    return JSONResponse(
        {
            "languages": languages,
            "experiences": experiences,
            "specialities": specialities,
        },
    )


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
