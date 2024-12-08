from pydantic import BaseModel

from core.data.models.employee_model import LineModel
from core.data.models.hour_by_hour_model import PlatformModel


class CycleModel(BaseModel):
    type: str
    start: float
    end: float
    time: float
    date: str

class CycleTimeInputModel(BaseModel):

    id: str
    line: LineModel
    platform: PlatformModel
    cycles: list[CycleModel]

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