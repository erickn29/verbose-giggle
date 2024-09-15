from typing import Annotated
from uuid import UUID

from apps.v1.vacancy.model import Experience, Language, Speciality
from apps.v1.vacancy.schema import (
    ResumeCreateSchema,
    ResumeListOutputSchema,
    ResumeOutputSchema,
    VacancyCreateSchema,
    VacancyListOutputSchema,
    VacancyOutputSchema,
)
from apps.v1.vacancy.service import ResumeService, VacancyService
from core.database import db_conn
from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse


router = APIRouter()


@router.get("/vacancy/", response_model=VacancyListOutputSchema)
async def vacancy_list(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
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


@router.get("/vacancy/selectors/")
async def vacancy_selectors():
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


@router.get("/vacancy/{vacancy_id}/", response_model=VacancyOutputSchema)
async def vacancy_detail(
    vacancy_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.get_schema(vacancy_id)


@router.post("/vacancy/", response_model=VacancyOutputSchema, status_code=201)
async def create_vacancy(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    data: Annotated[VacancyCreateSchema, Body(...)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.create(data)


@router.put(
    "/vacancy/{vacancy_id}/", response_model=VacancyOutputSchema, status_code=201
)
async def update_vacancy(
    vacancy_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    data: Annotated[VacancyCreateSchema, Body(...)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.update(vacancy_id, data)


@router.delete("/vacancy/{vacancy_id}/", status_code=204)
async def delete_vacancy(
    vacancy_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
):
    vacancy_service = VacancyService(session)
    return await vacancy_service.delete(vacancy_id)


@router.get("/resume/", response_model=ResumeListOutputSchema, status_code=200)
async def resume_list(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    request: Request,
    page: int = 1,
):
    resume_service = ResumeService(session)
    filters = {}
    params = request.query_params.items()
    for key, value in params:
        if key != "page" and value:
            filters[key] = value
    return await resume_service.fetch(
        pagination={"current_page": page, "limit": 20},
        filters=filters,
    )


@router.post("/resume/", response_model=ResumeOutputSchema, status_code=201)
async def create_resume(
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    data: Annotated[ResumeCreateSchema, Body(...)],
):
    resume_service = ResumeService(session)
    return await resume_service.create(data)
