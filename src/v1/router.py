from fastapi import APIRouter
from v1.user.router.router import router as user_router

v1_routers = APIRouter(prefix="/api/v1")

router_list = [
    (user_router, "/user", ["Пользователи"]),
    # (auth_router, "/auth", ["Аутентификация"]),
    # (page_router, "/page", ["Страницы"]),
    # (project_router, "/project", ["Проекты"]),
    # (stand_router, "/stand", ["Стенд"]),
    # (stand_page_router, "/stand-page", ["StandPage"]),
]

for router, prefix, tags in router_list:
    v1_routers.include_router(router, prefix=prefix, tags=tags)
