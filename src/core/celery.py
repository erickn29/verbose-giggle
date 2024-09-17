from celery import Celery
from celery.schedules import crontab
from core.settings import settings


celery_app = Celery(
    "worker",
    broker=f"redis://{settings.redis.HOST}:{settings.redis.PORT}/{settings.redis.DB}",
    backend=f"redis://{settings.redis.HOST}:{settings.redis.PORT}/{settings.redis.DB}",
    include=["tasks.parse"],
)


celery_app.conf.beat_schedule = {
    "PARSER: START": {
        "task": "tasks.parse.start_parsing",
        "schedule": crontab(minute="18", hour="14"),
    }
}


celery_app.conf.timezone = "Europe/Moscow"
