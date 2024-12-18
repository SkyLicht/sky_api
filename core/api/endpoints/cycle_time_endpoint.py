from datetime import date, datetime
from io import BytesIO
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from openpyxl.workbook import Workbook
from pydantic import BaseModel, Field, field_validator
from starlette.responses import StreamingResponse

from core.data.repositories.cycle_time.cycle_time_repository import CycleTimeRepository
from core.db.database import get_scoped_db_session

router = APIRouter(
    prefix="/cycle_time",
    tags=["cycle_time"]
)


def get_cycle_time_repository(db=Depends(get_scoped_db_session)):
    return CycleTimeRepository(db)


class CreateRecordRequest(BaseModel):
    str_date: Optional[str] = Field(None, description="Start date in YYYY-MM-DD format")
    week: Optional[int] = Field(None, description="Week number")
    line: Optional[str] = Field(None, description="Production line identifier")
    platform: Optional[str] = Field(None, description="Platform identifier")

    @property
    def body(self):
        return {
            "str_date": self.str_date,
            "week": self.week,
            "line": self.line,
            "platform": self.platform,
        }

    @field_validator('str_date', mode='before')
    def validate_str_date(cls, value):
        if value is None:
            return value  # Allow None if the field is optional
        try:
            # Attempt to parse the date
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("str_date must be in YYYY-MM-DD format")
        return value


class UpdateCycleTimeRequest(BaseModel):
    cycle_time_id: str = Field(None, description="Record ID")
    cycles: list[dict] = Field(None, description="Cycle times")


@router.post("/create/")
async def create_record(
        request: CreateRecordRequest,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):
    # Create a record
    try:
        record = await repository.create_record(request)

        return {
            "id": record.id,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_by_week")
async def get_by_week(
        year: int,
        week: int,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):
    # Get all records for a week
    try:
        records = await repository.get_by_week(week)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return records


@router.get("/get_by_week_details")
async def get_by_week(
        year: int,
        week: int,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):
    # Get all records for a week
    try:
        records = await repository.get_by_week_details(week)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return records


@router.get("/get_by_id")
async def get_by_id(
        record_id: str,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):
    # Get a record by ID
    try:
        record = await repository.get_by_id(record_id)
        return record
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_by_id_details")
async def get_by_id_details(
        record_id: str,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):
    # Get a record by ID
    try:
        record = await repository.get_by_id_details(record_id)
        return record
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete")
async def delete_record(
        record_id: str,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):
    # Delete a record by ID
    try:
        await repository.delete_record(record_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "ok",
        "message": "Record deleted",
    }


@router.patch('/update_cycle_time')
async def update_cycle_time(
        body: UpdateCycleTimeRequest,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):  # Update a cycle time
    try:
        await repository.update_cycle_time(body.cycle_time_id, body.cycles)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "ok",
        "message": "Cycle time updated",
    }


@router.get("/download_by_id")
async def download_by_id(
        record_id: str,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):  # Download a record by ID
    try:

        record = await repository.get_by_id_details(record_id)


        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Cycle Times"
        sheet.append(["line", 'area', "station", "ct"])

        for cycle in record['cycle_times']:
            sheet.append(
                [record['line'], cycle['section_name'], cycle['station'], cycle['average']]
            )


        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=cycle_times.xlsx"},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/lines_details_by_week")
async def lines_details_by_week(
        week: int,
        repository: CycleTimeRepository = Depends(get_cycle_time_repository),
):
    # Get all records for a week
    try:
        records = await repository.get_by_week_details_group_lines(week)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return records