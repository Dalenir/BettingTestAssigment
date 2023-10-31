from sqlalchemy import Column, String

from app.adapters.postgres import Base


class EventStateModel(Base):

    __tablename__ = "event_states"

    state = Column(String, primary_key=True)
