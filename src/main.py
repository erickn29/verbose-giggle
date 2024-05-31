from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from core.config import cfg


app = FastAPI(
    title="Python Russia",
    version="0.0.1",
    default_response_class=ORJSONResponse,
    docs_url="/swagger/" if cfg.DEBUG else None,
    redoc_url="/redoc/" if cfg.DEBUG else None,
    debug=cfg.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.CORS_ALLOWED_HOSTS,
    allow_credentials=cfg.CORS_ALLOWED_CREDENTIALS,
    # allow_origin_regex=cfg.CORS_ALLOWED_HOSTS_REGEX,
    allow_methods=cfg.CORS_ALLOWED_METHODS,
    allow_headers=cfg.CORS_ALLOWED_HEADERS,
)


@app.get("/")
async def root():
    return {"message": cfg.SECRET_KEY}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
