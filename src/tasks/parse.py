import asyncio

from typing import Any

from apps.v1.vacancy.utils.parser.head_hunter import HeadHunterParser
from core.celery import celery_app


async def run_async_parsing(parser_obj: Any):
    await parser_obj.get_vacancies()


async def parsing():
    hh_parser = HeadHunterParser()
    tasks = [run_async_parsing(hh_parser)]
    await asyncio.gather(*tasks)


@celery_app.task
def start_parsing():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(parsing())
    else:
        loop.run_until_complete(parsing())
