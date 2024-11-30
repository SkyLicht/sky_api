from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo



class WorkPlanQuery(BaseModel):
    line: Optional[str] = Field(None, description="Production line identifier")
    start_date: Optional[date] = Field(None, description="Start date in YYYY-MM-DD format")
    end_date: Optional[date] = Field(None, description="End date in YYYY-MM-DD format")
    factory: Optional[str] = Field(None, description="Factory identifier")

    @field_validator('start_date', 'end_date', mode='before')
    def parse_dates(cls, v, info: ValidationInfo):
        if isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @model_validator(mode='after')
    def validate_parameters(self):
        if not any([self.start_date, self.end_date, self.line]):
            raise ValueError('At least one of start_date, end_date, or line must be provided.')
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError('end_date must be after start_date')
        return self