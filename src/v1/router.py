from fastapi import APIRouter
from v1.user.router.router import router as user_router
from v1.vacancy.router.resume_router import router as resume_router
from v1.vacancy.router.vacancy_router import router as vacancy_router


v1_routers = APIRouter(prefix="/api/v1")

router_list = [
    (user_router, "/user", ["Пользователи"]),
    (vacancy_router, "/vacancy", ["Вакансии"]),
    (resume_router, "/resume", ["Резюме"]),
]

for router, prefix, tags in router_list:
    v1_routers.include_router(router, prefix=prefix, tags=tags)
