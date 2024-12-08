from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo



class GetHbhQuery(BaseModel):
    year: Optional[int] = Field(None, description="Year")
    week: Optional[int] = Field(None, description="Week number")
    line: Optional[str] = Field(None, description="Production line identifier")
    start_date: Optional[date] = Field(None, description="Start date in YYYY-MM-DD format")
    end_date: Optional[date] = Field(None, description="End date in YYYY-MM-DD format")
    factory: Optional[str] = Field(None, description="Factory identifier")

    result_type: Optional[str] = Field(None, description="Type of result to return")

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
        if not any([self.factory]):
            raise ValueError('At least one of factory must be provided.')
        if not any([self.line]):
            raise ValueError('At least one of line must be provided.')

        if not any([self.start_date, self.end_date, self.week]):
            raise ValueError('At least one of start_date, end_date, or week must be provided.')
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError('end_date must be after start_date')
        if self.week:
            if not self.year:
                raise ValueError('When week year must be provided.')
        return self