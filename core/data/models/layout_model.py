from typing import Optional

from pydantic import BaseModel, Field

from core.data.models.cycle_time_model import CycleTimeModel
from core.data.schemas.all_schemas import CycleTimeSchema


class LayoutModel(BaseModel):
    id: str = Field(..., max_length=16, description="Unique identifier for the layout")
    index: int = Field(..., description="Index of the layout")
    is_ct: bool = Field(default=False, description="Indicator if it's a CT layout")
    version: int = Field(..., description="Version of the layout")

    # Foreign Keys
    station_id: str = Field(..., max_length=16, description="ID of the station associated with the layout")
    cluster_id: Optional[str] = Field(None, max_length=16, description="ID of the cluster associated with the layout")
    line_id: str = Field(..., max_length=16, description="ID of the line associated with the layout")
    machine_id: Optional[str] = Field(None, max_length=16, description="ID of the machine associated with the layout")
    layout_section_id: str = Field(..., max_length=16, description="ID of the layout section associated with the layout")


    @staticmethod
    def from_schema(schema)-> 'LayoutModel':
        return LayoutModel(
            id=schema.id,
            index=schema.index,
            is_ct=schema.is_ct,
            version=schema.version,
            station_id=schema.station_id,
            cluster_id=schema.cluster_id,
            line_id=schema.line_id,
            machine_id=schema.machine_id,
            layout_section_id=schema.layout_section_id
        )

    def to_cycle_time_schema(self, cycles: list[CycleTimeModel])-> CycleTimeSchema:
        return CycleTimeSchema(
            cycles= cycles,
            layout_id=  self.id,
        )

