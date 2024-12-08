from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, Request
from openpyxl.workbook import Workbook
from starlette.responses import StreamingResponse

from core.api.fast_util import validate_date_range
from core.api.querys.hbh_query import GetHbhQuery
from core.data.models.request_model import RequestWeekEffModel
from core.data.repositories.hbhRepo import HourByHourRepository
from core.db.database import get_scoped_db_session
from core.logger.logger import Logger
from core.util import date_str_date_to_excel_date, ExcelDateType

_logger = Logger.get_logger(name="FastApi")
router = APIRouter(
    prefix="/hbh",
    tags=["hbh"]
)


# Dependency to get the repository
def get_hbh_repository(db=Depends(get_scoped_db_session)):
    return HourByHourRepository(db, _logger)


@router.get("/get_hbh")
async def get_hbh(
        request: Request,
        query: GetHbhQuery = Depends(),
        repo: HourByHourRepository = Depends(get_hbh_repository),
):
    try:
        # Execute the query and return the result
        _logger.info(f"[user] [{request.client[0]}] : Querying data for {query}")
        data = await repo.get_hour_by_hour_by(query=query)

        if data is None:
            raise HTTPException(status_code=400, detail=str("No data found"))

        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_hbh_excel")
async def get_hbh(
        request: Request,
        query: GetHbhQuery = Depends(),
        repo: HourByHourRepository = Depends(get_hbh_repository),
):
    try:
        # Execute the query and return the result
        _logger.info(f"[user] [{request.client[0]}] : Querying data for {query}")
        data = await repo.get_hour_by_hour_by(query=query)

        if data:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Hour by Hour"
            sheet.append(["factory", "date", "week", "line", "hour", "smt_in", "smt_out", "packing"])
            for record in data:
                sheet.append(
                    [record.factory,
                     date_str_date_to_excel_date(record.date, ExcelDateType.SHORT_DATE),
                     record.week,
                     record.line,
                     record.hour,
                     record.smt_in, record.smt_out, record.packing])

            buffer = BytesIO()
            workbook.save(buffer)
            buffer.seek(0)

            return StreamingResponse(
                buffer,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=hourly_data.xlsx"},
            )
        else:
            raise HTTPException(status_code=400, detail=str("No data found"))






    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get_eff_by_week")
async def get_eff_by_week(
        body: RequestWeekEffModel,
        repo: HourByHourRepository = Depends(get_hbh_repository),

):
    try:
        if body is None:
            raise HTTPException(status_code=400, detail=str("No data provided"))
        return await repo.get_kpi_by_week(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update_day_before")
async def update_day_before(
        repo: HourByHourRepository = Depends(get_hbh_repository),
):
    try:

        await repo.update_previews_day()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "ok", "message": "Day before updated", "data": []}


@router.get("/update_range_of_dates")
async def update_range_of_dates(
        start_date: str,
        end_date: str,
        repo: HourByHourRepository = Depends(get_hbh_repository),

):
    """
    Updates data for a given range of dates after validating the date range.
    """
    # Validate the date range using the utility function
    try:
        start_date_obj, end_date_obj = validate_date_range(start_date, end_date)
    except HTTPException as e:
        raise e

        # Proceed with updating the range
    try:
        await repo.update_range_of_dates(start_date_obj.strftime("%Y-%m-%d"),
                                         end_date_obj.strftime("%Y-%m-%d"))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating: {e}"
        )

    return {"status": "ok", "data": True}
