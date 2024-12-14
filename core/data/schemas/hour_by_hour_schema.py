from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from core.db.database import Base
from core.db.util import generate_16_uuid

class PlatformSchema(Base):
    __tablename__ = 'platforms'
    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    sku = Column(String(5), nullable=False)
    name = Column(String(50), nullable=False)
    uph = Column(Integer, nullable=False)
    f_n = Column(Float, nullable=False, default=0.0)
    heller_t = Column(JSON, nullable=True)

    # Relationship to WorkPlan
    work_plans = relationship("WorkPlanSchema", back_populates="platforms")
    # cycle_times = relationship("CycleTimeSchema",backref ="platforms")

    def to_json(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "uph": self.uph,
            "f_n": self.f_n,
            "heller_t": self.heller_t
        }

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "uph": self.uph,
            "f_n": self.f_n,
            "heller_t": self.heller_t
        }

    def to_dic_short(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "uph": self.uph,
            "f_n": self.f_n,
        }




class WorkPlanSchema(Base):
    __tablename__ = 'work_plans'
    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    factory = Column(String(10), nullable=False)
    line = Column(String(3), nullable=False)
    date = Column(String(10), nullable=False)
    uph_i = Column(Integer, nullable=False)
    target_oee = Column(Float, nullable=False)
    planned_hours = Column(Float, nullable=False)
    week = Column(Integer, nullable=False)
    state = Column(String(10), nullable=False)


    # Foreign key to Platform
    platform_id = Column(String(16), ForeignKey('platforms.id'), nullable=False)


    #created date
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship to Platform
    platforms = relationship("PlatformSchema", back_populates="work_plans")





    def to_dict(self):
        return {
            "id": self.id,
            "line": self.line,
            "date": self.date,
            "uph_i": self.uph_i,
            "target_oee": self.target_oee,
            "planned_hours": self.planned_hours,
            "week": self.week,
            "state": self.state
        }

    def to_dic_short(self):
        return {
            "line": self.line,
            "date": self.date,
            "uph_i": self.uph_i,
            "target_oee": self.target_oee,
            "planned_hours": self.planned_hours,
            "week": self.week,
            "state": self.state
        }


class HourByHourSchema(Base):
    __tablename__ = 'hour_by_hour'
    __table_args__ = (
        UniqueConstraint('factory', 'line' ,'date','hour', name='unique_hbh_record_factory'),
    )


    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    factory = Column(String(10), nullable=False)
    line = Column(String(3), nullable=False)
    date = Column(String(10), nullable=False)
    hour = Column(Integer, nullable=False)
    smt_in = Column(Integer, nullable=False)
    smt_out = Column(Integer, nullable=False)
    packing = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "factory": self.factory,
            "line": self.line,
            "date": self.date,
            "hour": self.hour,
            "smt_in": self.smt_in,
            "smt_out": self.smt_out,
            "packing": self.packing
        }

