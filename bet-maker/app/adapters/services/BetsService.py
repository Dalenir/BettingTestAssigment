from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.postgres import AlchemyMaster
from app.adapters.postgres.models.BetModel import BetModel
from app.adapters.postgres.models.BetResultModel import BetResultModel
from app.adapters.shemas import BetBasic, Event, EventState
from app.adapters.shemas.Bet import BetResult, Bet


@AlchemyMaster.alchemy_session
async def bet_on_event(bet: BetBasic, *, alchemy_session: AsyncSession):
    query = insert(BetModel).values(**bet.model_dump(mode='json')).returning(BetModel)
    result = (await alchemy_session.execute(query)).scalar()
    await alchemy_session.commit()
    if result:
        return Bet.model_validate(result)


@AlchemyMaster.alchemy_session
async def update_bets_result(event: Event, *, alchemy_session: AsyncSession):
    target_bets = (await alchemy_session.execute(select(BetModel).where(BetModel.event_id == event.id))).scalars().all()
    for bet in target_bets:
        result = BetResult.WINNER if EventState(bet.event_state) == event.state else BetResult.LOSER

        result_obj = await alchemy_session.get(BetResultModel, result.value)
        if not result_obj:
            result_obj = BetResultModel(state=result.value)
            await alchemy_session.merge(result_obj)
            await alchemy_session.flush()

        bet.result = result.value
        await alchemy_session.merge(bet)
        await alchemy_session.flush()

    await alchemy_session.commit()


@AlchemyMaster.alchemy_session
async def get_bets_list(*, alchemy_session: AsyncSession):
    return (await alchemy_session.execute(select(BetModel))).scalars().all()
