from datetime import datetime

from core.db.database import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint, Table, DateTime, JSON
from sqlalchemy.orm import relationship
from core.db.util import generate_16_uuid


class CycleTimeSchema(Base):
    __table__ = 'cycle_times'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)

    cycles = Column(JSON, nullable=False, default=list)

    created_at = Column(DateTime, nullable=False, default = datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)




    line_id = Column(Integer, ForeignKey('lines.id'), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)





    line = relationship('LineSchema', backref='cycle_times')
    platform = relationship('PlatformSchema', backref='cycle_times')




