import asyncio
import time

import pytest
import pytest_asyncio

from app.adapters.postgres import AlchemyMaster, EventModel
from settings import get_api_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
def database_setup(settings=get_api_settings()):
    AlchemyMaster.prepare_engine(pg_username=settings.POSTGRES_USER,
                                 pg_password=settings.POSTGRES_PASSWORD,
                                 pg_host=settings.POSTGRES_HOST,
                                 pool=False)
    yield


@pytest_asyncio.fixture(scope='session', autouse=True)
async def database_filling(database_setup):
    session_connect = await AlchemyMaster.create_session()

    data = [
        EventModel(
            id="145",
            coefficient=0.11,
            deadline=time.time() + 120,
            state="New"
        ),
        EventModel(
            id="hhhh",
            coefficient=9,
            deadline=time.time() + 120,
            state="New"
        ),
        EventModel(
            id="1234",
            coefficient=22.25,
            deadline=time.time() + 120,
            state="New"
        ),
        EventModel(
            id="ZZZ",
            coefficient=66.11,
            deadline=time.time() + 120,
            state="New"
        ),
    ]

    async with session_connect() as session:
        for event in data:
            await session.merge(event)

        await session.commit()
