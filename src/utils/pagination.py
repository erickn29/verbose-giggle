from math import ceil

from pydantic import BaseModel
from repository.alchemy_orm import SQLAlchemyRepository


class PaginationSchema(BaseModel):
    count: int
    maxPage: int
    currentPage: int
    limit: int


async def paginate(
    paginate_dict: dict,
    filters: dict,
    repository: SQLAlchemyRepository,
) -> dict:
    if not paginate_dict:
        paginate_dict = {"current_page": 1, "limit": 20}
    not_paginated_data = await repository.fetch(filters=filters)
    paginated_data = await repository.fetch(filters=filters, paginate=paginate_dict)
    return {
        "pagination": PaginationSchema(
            count=len(not_paginated_data),
            maxPage=ceil(len(not_paginated_data) / paginate_dict["limit"]),
            currentPage=paginate_dict.get("current_page"),
            limit=paginate_dict.get("limit"),
        ),
        "result": paginated_data,
    }
