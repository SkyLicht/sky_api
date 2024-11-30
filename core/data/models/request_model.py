from pydantic import BaseModel


class RequestWeekEffLinesModel(BaseModel):
    name: str
    output: str
    shift: str

class RequestWeekEffDatesModel(BaseModel):
    day : str
    lines: list[RequestWeekEffLinesModel]

class RequestWeekEffModel(BaseModel):
    year: int
    week: int
    dates: list[RequestWeekEffDatesModel]
