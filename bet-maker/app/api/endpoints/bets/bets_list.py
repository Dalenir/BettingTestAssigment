from app.adapters.services import BetsService
from ._router import bets_router


@bets_router.get("/bets")
async def bets():
    return await BetsService.get_bets_list()
