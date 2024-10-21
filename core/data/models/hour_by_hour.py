from sqlalchemy import Column, Integer, String

from core.db.database import Base
from core.db.util import generate_short_uuid


class HourByHour(Base):
    __tablename__ = 'hour_by_hour'
    id = Column(String(36), primary_key=True, default=lambda: str(generate_short_uuid()), unique=True, nullable=False)
    line = Column(String(3), nullable=False)
    date = Column(String(10), nullable=False)
    hour = Column(Integer, nullable=False)
    smt_in = Column(Integer, nullable=False)
    smt_out = Column(Integer, nullable=False)
    packing = Column(Integer, nullable=False)
