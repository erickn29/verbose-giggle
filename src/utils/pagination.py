from math import ceil

from base.repository import BaseRepository
from pydantic import BaseModel


class PaginationSchema(BaseModel):
    count: int
    maxPage: int
    currentPage: int
    limit: int


async def paginate(
    paginate_dict: dict,
    filters: dict,
    repository: BaseRepository,
) -> dict:
    if not paginate_dict:
        paginate_dict = {"current_page": 1, "limit": 20}
    not_paginated_data = await repository.filter(filters=filters)
    paginated_data = await repository.filter(filters=filters, paginate=paginate_dict)
    return {
        "pagination": PaginationSchema(
            count=len(not_paginated_data),
            maxPage=ceil(len(not_paginated_data) / paginate_dict["limit"]),
            currentPage=paginate_dict.get("current_page"),
            limit=paginate_dict.get("limit"),
        ),
        "result": paginated_data,
    }
