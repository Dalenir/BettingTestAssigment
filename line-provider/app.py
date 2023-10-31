import enum
import time
from typing import Optional

from fastapi import FastAPI, Path, HTTPException, Query, Depends
from pydantic import BaseModel, field_validator


class EventState(enum.Enum):
    NEW = 'New'
    FINISHED_LOSE = 'Lose'
    FINISHED_WIN = 'Win'


class Event(BaseModel):
    id: str | int
    coefficient: Optional[float] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None

    @field_validator('coefficient')
    def name_must_contain_space(cls, v):
        if v <= 0:
            raise ValueError('coefficient must be greater than 0')
        return round(v, 2)


events: dict[str, Event] = {
    '1': Event(id='1', coefficient=1.2, deadline=int(time.time()) + 600, state=EventState.NEW),
    '2': Event(id='2', coefficient=1.15, deadline=int(time.time()) + 60, state=EventState.NEW),
    '3': Event(id='3', coefficient=1.67, deadline=int(time.time()) + 90, state=EventState.NEW),
    '4': Event(id='1', coefficient=1.2, deadline=int(time.time()) + 600, state=EventState.NEW),
    '5': Event(id='2', coefficient=1.33, deadline=int(time.time()) + 60, state=EventState.FINISHED_WIN),
    '6': Event(id='3', coefficient=1.67, deadline=int(time.time()) + 90, state=EventState.FINISHED_LOSE)
}

app = FastAPI(docs_url="/docs")

@app.put('/event')
async def upsert_event(event: Event):
    if event.id not in events:
        events[event.id] = event
        return "Succsessfully created event"
    else:
        events[event.id] = event
        return "Succsessfully updated event"


@app.get('/event/{event_id}')
async def get_event(event_id: str = Path()):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")


class EventsRequest(BaseModel):
    events_ids: list[str] = Query(Query(default=[]))


@app.get('/events')
async def get_events(data: EventsRequest = Depends()):
    for event in events.values():
        print(event, time.time() < event.deadline, event.id in data.events_ids)
    if not data.events_ids:
        return list(e for e in events.values() if time.time() < e.deadline)
    else:
        return list(e for e in events.values() if time.time() < e.deadline or e.id in data.events_ids)
