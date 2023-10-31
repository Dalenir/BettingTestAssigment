import enum

from pydantic import field_validator

from app.adapters.shemas.Event import EventState
from app.adapters.shemas._model import Model


class BetResult(enum.Enum):
    WAITING = 'Waiting for result'
    LOSER = 'Loser'
    WINNER = 'Winner'


class BetBasic(Model):
    event_id: str
    bet_amount: float
    bet_on_event_state: EventState

    @field_validator('bet_on_event_state')
    def name_must_contain_space(cls, v):
        if v == EventState.NEW:
            raise ValueError('You can bet only at "Win" or "Lose" event states.')
        return v


class Bet(BetBasic):
    id: str | int


class BetFinal(BetBasic):
    state: BetResult = BetResult.WAITING
