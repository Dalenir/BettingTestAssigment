from app.adapters.postgres import Base
from .BetResultModel import BetResultModel
from .EventStateModel import EventStateModel

from sqlalchemy import Column, ForeignKey, String, Float, Integer


class BetModel(Base):

    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String, nullable=False)
    bet_amount = Column(Float, nullable=False)
    bet_on_event_state = Column(String, ForeignKey(EventStateModel.state), nullable=False)
    result = Column(String, ForeignKey(BetResultModel.state, ondelete="CASCADE", onupdate="CASCADE"),
                    nullable=True, default=None)
