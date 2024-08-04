from typing import Annotated

from core.database import get_async_session
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from v1.vacancy.schema.schema import ResumeCreateSchema, ResumeOutputSchema, \
    ResumeListOutputSchema
from v1.vacancy.service.service import ResumeService


router = APIRouter()


@router.get("/", response_model=ResumeListOutputSchema, status_code=200)
async def resume_list(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    request: Request,
    page: int = 1,
):
    resume_service = ResumeService(session)
    filters = {}
    params = request.query_params.items()
    for key, value in params:
        if key != "page" and value:
            filters[key] = value
    return await resume_service.all(
        pagination={"current_page": page, "limit": 20},
        filters=filters,
    )


@router.post("/", response_model=ResumeOutputSchema, status_code=201)
async def create_resume(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: Annotated[ResumeCreateSchema, Body(...)],
):
    resume_service = ResumeService(session)
    return await resume_service.create(data)
