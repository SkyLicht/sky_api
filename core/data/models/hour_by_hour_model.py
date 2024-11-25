from pydantic import BaseModel

from core.data.schemas.hour_by_hour_schema import HourByHourSchema


class HourByHourModel(BaseModel):
    id: str = None
    line: str
    date: str
    hour: int
    smt_in: int
    smt_out: int
    packing: int

    def to_schema(self)-> HourByHourSchema:
        return HourByHourSchema(
            line=self.line,
            date=self.date,
            hour=self.hour,
            smt_in=self.smt_in,
            smt_out=self.smt_out,
            packing=self.packing
        )

    def to_dict(self):
        return {
            "id": self.id,
            "line": self.line,
            "date": self.date,
            "hour": self.hour,
            "smt_in": self.smt_in,
            "smt_out": self.smt_out,
            "packing": self.packing
        }

    def __str__(self):
        return str(self.to_dict())


class PlatformModel(BaseModel):
    id: str = None
    sku: str
    name: str
    uph: int
    f_n: float
    heller_t: dict

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "uph": self.uph,
            "f_n": self.f_n,
            "heller_t": self.heller_t
        }

    def __str__(self):
        return str(self.to_dict())


class WorkPlanModel(BaseModel):
    id: str = None
    line: str
    date: str
    uph_i: int
    target_ooe: float
    planned_hours: float
    week: int
    state: int
    platform_id: str

    def to_dict(self):
        return {
            "id": self.id,
            "line": self.line,
            "date": self.date,
            "uph_i": self.uph_i,
            "target_ooe": self.target_ooe,
            "planned_hours": self.planned_hours,
            "week": self.week,
            "state": self.state,
            "platform_id": self.platform_id
        }

    def __str__(self):
        return str(self.to_dict())