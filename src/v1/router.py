from fastapi import APIRouter
from v1.user.router.router import router as user_router
from v1.vacancy.router.router import router as vacancy_router


v1_routers = APIRouter(prefix="/api/v1")

router_list = [
    (user_router, "/user", ["Пользователи"]),
    (vacancy_router, "/vacancy", ["Вакансии"]),
    # (page_router, "/page", ["Страницы"]),
    # (project_router, "/project", ["Проекты"]),
    # (stand_router, "/stand", ["Стенд"]),
    # (stand_page_router, "/stand-page", ["StandPage"]),
]

for router, prefix, tags in router_list:
    v1_routers.include_router(router, prefix=prefix, tags=tags)
