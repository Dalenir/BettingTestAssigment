import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.postgres import AlchemyMaster, EventModel
from app.adapters.services import BetsService, EventsService
from app.adapters.shemas import EventState
from app.adapters.shemas.Event import Event
from settings import get_api_settings

async_sheduler = AsyncIOScheduler(timezone='UTC')


@AlchemyMaster.alchemy_session
async def update_events_bets(settings=get_api_settings(), *, alchemy_session: AsyncSession):
    async with (aiohttp.ClientSession() as session):

        not_finished_events = (await alchemy_session.execute(
            select(EventModel.id).where(EventModel.state == EventState.NEW.value)
        )).scalars().all()

        async with session.get(settings.events_api_url + '/events',
                               params={"events_ids": not_finished_events}
                               ) as response:
            if response.status == 200:
                events = [Event.model_validate(event_data) for event_data in await response.json()]
                for event in events:
                    #  Btw that's why I love my decorator: it's make all much more flexible!
                    await EventsService.update_event_data(event=event, alchemy_session=alchemy_session)
                    if event.state != EventState.NEW:
                        await BetsService.update_bets_result(event=event)
                await alchemy_session.commit()


def switch_events_updating(set_events_updating: bool):
    task_name = 'update_events'
    if not set_events_updating and async_sheduler.get_job(task_name):
        async_sheduler.remove_job(task_name)
    else:
        async_sheduler.add_job(update_events_bets, 'interval', seconds=3, id=task_name)
        async_sheduler.start()
