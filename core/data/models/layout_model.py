from typing import Optional

from pydantic import BaseModel, Field


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

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy ORM models
