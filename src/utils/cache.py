import datetime
import json

from uuid import UUID

import redis.asyncio as redis

from core.exceptions import exception
from core.settings import settings
from redis import RedisError
from schemas.user import UserModelSchema


class Cache:
    def __init__(
        self, host=settings.redis.HOST, port=settings.redis.PORT, db=settings.redis.DB
    ):
        self.host = host
        self.port = port
        self.db = db
        self.connection_pool = redis.ConnectionPool(
            host=self.host, port=self.port, db=self.db
        )
        self.redis_cache = redis.StrictRedis(connection_pool=self.connection_pool)

    async def set(self, key: str, value: str, expire: int = 60):
        try:
            await self.redis_cache.set(key, value, expire)
        except RedisError as e:
            raise exception(400, "Ошибка сохранения данных в кэш", str(e)) from e

    async def get(self, key, decode="utf-8"):
        res = await self.redis_cache.get(key)
        if res:
            return res.decode(decode)
        return res

    async def delete(self, key: str):
        await self.redis_cache.delete(key)

    async def set_user(self, schema: UserModelSchema):
        schema.id = str(schema.id)
        schema.created_at = schema.created_at.strftime("%Y-%m-%d %H:%M:%S")
        schema.updated_at = schema.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        schema_string = json.dumps(schema.model_dump())
        await self.set(
            f"user:{str(schema.id)}",
            schema_string,
            settings.auth.ACCESS_TOKEN_EXPIRE - 10,
        )

    async def get_user(self, id: str) -> UserModelSchema | None:
        res = await self.get(f"user:{id}")
        if res:
            schema = UserModelSchema.model_validate(json.loads(res))
            schema.id = UUID(schema.id)
            schema.created_at = datetime.datetime.strptime(
                schema.created_at,
                "%Y-%m-%d %H:%M:%S",
            )
            schema.updated_at = datetime.datetime.strptime(
                schema.updated_at,
                "%Y-%m-%d %H:%M:%S",
            )
            return UserModelSchema.model_validate(schema)
        return None


cache = Cache()
