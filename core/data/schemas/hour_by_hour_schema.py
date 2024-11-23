from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship

from core.db.database import Base
from core.db.util import generate_short_uuid

class PlatformSchema(Base):
    __tablename__ = 'platform'
    id = Column(String(16), primary_key=True, default=lambda: str(generate_short_uuid()), unique=True, nullable=False)
    sku = Column(String(5), nullable=False)
    name = Column(String(50), nullable=False)
    uph = Column(Integer, nullable=False)
    f_n = Column(Float, nullable=False, default=0.0)
    heller_t = Column(JSON, nullable=True)

    # Relationship to WorkPlan
    work_plans = relationship("WorkPlanSchema", back_populates="platform")


class WorkPlanSchema(Base):
    __tablename__ = 'work_plan'
    id = Column(String(16), primary_key=True, default=lambda: str(generate_short_uuid()), unique=True, nullable=False)
    line = Column(String(3), nullable=False)
    date = Column(String(10), nullable=False)
    uph_i = Column(Integer, nullable=False)
    target_ooe = Column(Float, nullable=False)
    planned_hours = Column(Float, nullable=False)
    head_count = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)

    # Foreign key to Platform
    platform_id = Column(String(16), ForeignKey('platform.id'), nullable=False)

    # Relationship to Platform
    platform = relationship("PlatformSchema", back_populates="work_plans")


class HourByHourSchema(Base):
    __tablename__ = 'hour_by_hour'
    id = Column(String(16), primary_key=True, default=lambda: str(generate_short_uuid()), unique=True, nullable=False)
    line = Column(String(3), nullable=False)
    date = Column(String(10), nullable=False)
    hour = Column(String(2), nullable=False)
    smt_in = Column(Integer, nullable=False)
    smt_out = Column(Integer, nullable=False)
    packing = Column(Integer, nullable=False)

    def to_dic(self):
        return {
            "id": self.id,
            "line": self.line,
            "date": self.date,
            "hour": self.hour,
            "smt_in": self.smt_in,
            "smt_out": self.smt_out,
            "packing": self.packing
        }

