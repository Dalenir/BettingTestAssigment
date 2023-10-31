from sqlalchemy import Column, String, Float, BigInteger, ForeignKey

from app.adapters.postgres import Base
from app.adapters.postgres.models.EventStateModel import EventStateModel


class EventModel(Base):

    __tablename__ = "events"

    id = Column(String, primary_key=True)
    coefficient = Column(Float)
    deadline = Column(BigInteger)
    state = Column(String, ForeignKey(EventStateModel.state), nullable=False)
