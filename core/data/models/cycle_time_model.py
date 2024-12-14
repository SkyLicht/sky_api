from datetime import datetime

from pydantic import BaseModel

from core.data.models.employee_model import LineModel
from core.data.models.hour_by_hour_model import PlatformModel
from core.data.schemas.all_schemas import CycleTimeSchema


class CycleTimeModel(BaseModel):
    type: str
    time: float
    created: str
    finished: str
    updated_at: str

    def to_dict(self):
        return {
            'type': self.type,
            'time': self.time,
            'create': self.created,
            'finished': self.finished,
            'updated_at': self.updated_at
        }

class CycleTimeInputModel(BaseModel):

    id: str
    str_date: str
    week: int
    line: LineModel
    platform: PlatformModel
    cycles: list[CycleTimeModel]

    created_at: datetime
    updated_at: datetime


    @staticmethod
    def cycles_to_json(cycles):
        return [cycle.to_json() for cycle in cycles]


    # @classmethod
    # def from_schema(cls,schema: CycleTimeSchema) -> 'CycleTimeInputModel':
    #     return cls(
    #         id=schema.id,
    #         line= LineModel.from_schema(schema.line),#LineModel.form_schema(schema.line),
    #         platform= PlatformModel.from_schema(schema.platform),#PlatformModel.form_schema(schema.platform)
    #         cycles=[CycleTimeModel(
    #             type=cycle['type'],
    #             start=cycle['start'],
    #             end=cycle['end'],
    #             time=cycle['time'],
    #             created=cycle['created']
    #         ) for cycle in schema.cycles],
    #         created_at=schema.created_at,
    #         updated_at=schema.updated_at
    #     )

    # def __init__(self, model: str):
    #     self.model = model
    #
    # def predict(self, data: List[Dict[str, Any]]) -> List[float]:
    #     return [random.uniform(1, 10) for _ in data]
    #
    # def save(self, path: str) -> None:
    #     with open(path, "w") as f:
    #         f.write(self.model)
    #
    # @staticmethod
    # def load(path: str) -> "CycleTimeModel":
    #     with open(path, "r") as f:
    #         model = f.read()
    #     return CycleTimeModel(model)
    #
    # @staticmethod
    # def load_default() -> "CycleTimeModel":
    #     return CycleTimeModel("default_model")
    #
    # def __eq__(self, other: Any) -> bool:
    #     return isinstance(other, CycleTimeModel) and self.model == other.model
    #
    # def __repr__(self) -> str:
    #     return f"CycleTimeModel(model={self.model})"