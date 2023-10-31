from pydantic import computed_field

from app.adapters.services import BetsService, EventsService
from app.adapters.shemas import EventState, Event
from app.adapters.shemas.Bet import BetBasic, Bet
from ._router import bet_router

from fastapi import HTTPException


class NewBetRequest(BetBasic):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "event_id": "Event id string",
                    "bet_amount": 2,
                    "bet_on_event_state": "Win"
                }
            ]
        }
    }


class NewBetResponse(Bet):

    event: Event

    @computed_field
    @property
    def payment_on_win(self) -> float:
        return self.bet_amount * self.event.coefficient


@bet_router.put("/bet")
async def bet(incoming_bet: NewBetRequest):
    event = await EventsService.get_one_event(incoming_bet.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.state != EventState.NEW:
        raise HTTPException(status_code=400, detail="You can't bet on finished event")
    if incoming_bet.bet_amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    new_bet: BetBasic = await BetsService.bet_on_event(incoming_bet)
    if new_bet:
        return NewBetResponse(**new_bet.model_dump(), event=event)
