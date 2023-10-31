from sqlalchemy import String, Column

from app.adapters.postgres import Base


class BetResultModel(Base):

    __tablename__ = "bet_states"

    state = Column(String, primary_key=True)
