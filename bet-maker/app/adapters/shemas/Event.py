import enum

from app.adapters.shemas._model import Model


class EventState(enum.Enum):
    NEW = 'New'
    FINISHED_LOSE = 'Lose'
    FINISHED_WIN = 'Win'


class Event(Model):
    id: str
    coefficient: float
    deadline: int
    state: EventState
