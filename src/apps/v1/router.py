from apps.v1.auth.router import router as router_auth
from apps.v1.interview.router import router as router_interview
from apps.v1.user.router import router as router_user
from apps.v1.vacancy.router import router as router_vacancy
from fastapi import APIRouter


router = APIRouter(prefix="/v1")


routes = (
    (
        router_auth,
        "/auth",
        [
            "Авторизация",
        ],
    ),
    (
        router_user,
        "/user",
        [
            "Пользователи",
        ],
    ),
    (
        router_vacancy,
        "/job",
        [
            "Вакансии и Резюме",
        ],
    ),
    (
        router_interview,
        "/interview",
        [
            "Интервью",
        ],
    ),
)


for route, prefix, tags in routes:
    router.include_router(router=route, prefix=prefix, tags=tags)
