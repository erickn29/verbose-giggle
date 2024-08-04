from factory.alchemy import SQLAlchemyModelFactory


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = None
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        async with cls._meta.sqlalchemy_session as session:
            await session.commit()
        return await instance

    @classmethod
    async def _save(cls, model_class, session, args, kwargs):
        obj = model_class(*args, **kwargs)
        session.add(obj)
        await session.commit()
        return obj
