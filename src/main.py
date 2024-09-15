import uvicorn

from apps.router import router as routers
from core.exceptions import BaseHTTPException
from core.settings import settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Python Russia",
    version="0.0.1",
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


@app.exception_handler(BaseHTTPException)
async def http_exception_handler(
    request: Request,
    exc: BaseHTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.get_response(),
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.HOST,
        port=settings.app.PORT,
        reload=True,
    )
