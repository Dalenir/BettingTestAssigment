from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.postgres import AlchemyMaster, EventModel, EventStateModel
from app.adapters.shemas import EventState, Event


@AlchemyMaster.alchemy_session
async def get_all_events(*, alchemy_session: AsyncSession):
    query = select(EventModel).where(EventModel.state == EventState.NEW.value)
    raw_events = (await alchemy_session.execute(query)).scalars().all()
    return [Event.model_validate(event) for event in raw_events]


@AlchemyMaster.alchemy_session
async def get_one_event(event_id: int, *, alchemy_session: AsyncSession):
    event = await alchemy_session.get(EventModel, event_id)
    return Event.model_validate(event)


@AlchemyMaster.alchemy_session
async def update_event_data(event: Event, *, alchemy_session: AsyncSession):
    state_obj = EventStateModel(state=event.state.value)
    await alchemy_session.merge(state_obj)
    await alchemy_session.flush()
    await alchemy_session.merge(EventModel(
        id=event.id,
        coefficient=event.coefficient,
        deadline=event.deadline,
        state=event.state.value
    ))
