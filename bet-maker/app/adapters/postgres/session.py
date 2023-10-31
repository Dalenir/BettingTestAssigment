import inspect as pyth_inspect

from sqlalchemy import inspect, NullPool, QueuePool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class AlchemyMaster:
    engine = None

    @classmethod
    def prepare_engine(cls, pg_username: str, pg_password: str, pg_host: str, pg_database: str = 'postgres',
                       pool: bool = True):
        cls.engine = create_async_engine(
            f"postgresql+asyncpg://{pg_username}:{pg_password}@{pg_host}/{pg_database}",
            poolclass=QueuePool if pool else NullPool
        )

    @staticmethod
    def _check_shemas(conn):
        inspector = inspect(conn)
        return inspector.get_schema_names()

    @classmethod
    async def create_session(cls):
        assert cls.engine, 'No engine is defined!'
        return async_sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=cls.engine,
                    class_=AsyncSession,
                    expire_on_commit=False
        )

    @classmethod
    def alchemy_session(cls, function):
        async def wrap(*args, **kwargs):

            if kwargs.get('alchemy_session'):
                return await function(*args, **kwargs)

            session_connect = await AlchemyMaster.create_session()
            async with session_connect() as session:
                kwargs['alchemy_session'] = session
                prepared_kwargs = {
                    k: v for k, v in kwargs.items()
                    if k in pyth_inspect.getfullargspec(function).args
                       or k in pyth_inspect.getfullargspec(function).kwonlyargs
                }
                return await function(*args, **prepared_kwargs)

        return wrap
