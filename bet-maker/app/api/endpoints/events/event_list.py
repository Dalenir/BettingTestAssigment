from app.adapters.services import EventsService
from ._router import events_router


@events_router.get("/events")
async def event_list():
    return await EventsService.get_all_events()
