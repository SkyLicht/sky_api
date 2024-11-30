from datetime import date
from typing import Optional

from pydantic import BaseModel


class WorkPlanResponse(BaseModel):
    line: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    factory: Optional[str]
    plan_details: str