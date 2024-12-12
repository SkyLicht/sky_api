from datetime import datetime

from core.data.schemas.employee_schema import LineSchema
from core.data.schemas.hour_by_hour_schema import PlatformSchema
from core.db.database import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint, Table, DateTime, JSON
from sqlalchemy.orm import relationship
from core.db.util import generate_16_uuid


class CycleTimeSchema(Base):
    __tablename__ = 'cycle_times'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    str_date = Column(String(10), nullable=False)
    week = Column(Integer, nullable=False)
    cycles = Column(JSON, nullable=False, default=list)

    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Foreign key to Platform
    line_id = Column(String(16), ForeignKey('lines.id'), nullable=False)
    platform_id = Column(String(16), ForeignKey('platforms.id'), nullable=False)

    # Deferred relationships: Ensure these classes are imported and available
    # Use backref to define bidirectional relationship
    line = relationship('LineSchema', backref='cycle_times')
    platform = relationship('PlatformSchema', backref='cycle_times')

    def to_json(self):
        return {
            'id': self.id,
            'str_date': self.str_date,
            'week': self.week,
            'cycles': self.cycles,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'line_id': self.line_id,
            'platform_id': self.platform_id,
            'line': self.line.to_json(),
            'platform': self.platform.to_json()
        }

    def __repr__(self):
        return f"CycleTimeSchema(id={self.id}, str_date={self.str_date}, week={self.week}, cycles={self.cycles}, " \
               f"created_at={self.created_at}, updated_at={self.updated_at}, line_id={self.line_id}, " \
               f"platform_id={self.platform_id}), line={self.line}, platform={self.platform}"

    @staticmethod
    def create_cycle_time_schema(str_date, week, cycles, line_id, platform_id) -> 'CycleTimeSchema':
        return CycleTimeSchema(str_date=str_date, week=week, cycles=cycles, line_id=line_id, platform_id=platform_id)
