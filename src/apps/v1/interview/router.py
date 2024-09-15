from fastapi import APIRouter


router = APIRouter()


@router.post("/q/")
async def send_question():
    """Генерирует и отправляет вопрос пользователю"""
    return {"status": "ok"}


@router.post("/a/")
async def get_answer():
    """Принимает ответ от пользователя и дает оценку"""
    return {"status": "ok"}
