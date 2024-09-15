from apps.router import router as routers
from core.settings import settings

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Python Russia",
    version="0.0.1",
    default_response_class=ORJSONResponse,
    docs_url="/swagger/" if settings.app.DEBUG else None,
    redoc_url="/redoc/" if settings.app.DEBUG else None,
    debug=settings.app.DEBUG,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.ALLOWED_HOSTS,
    allow_credentials=settings.cors.ALLOWED_CREDENTIALS,
    # allow_origin_regex=settings.CORS_ALLOWED_HOSTS_REGEX,
    allow_methods=settings.cors.ALLOWED_METHODS,
    allow_headers=settings.cors.ALLOWED_HEADERS,
)


app.include_router(routers)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.HOST,
        port=settings.app.PORT,
        reload=True,
    )
