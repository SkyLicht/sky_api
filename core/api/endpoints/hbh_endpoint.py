import re

from fastapi import APIRouter, Depends, HTTPException

from core.api.fat_util import validate_date_range
from core.data.repositories.hbhRepo import HourByHourRepository
from core.db.database import get_scoped_db_session

router = APIRouter(
    prefix="/hbh",
    tags=["hbh"]
)


# Dependency to get the repository
def get_hbh_repository(db=Depends(get_scoped_db_session)):
    return HourByHourRepository(db)


@router.post("/get_by_week")
async def read_by_week(
        body: dict,
        repo: HourByHourRepository = Depends(get_hbh_repository),

):
    try:
        if body is None:
            raise HTTPException(status_code=400, detail=str("No data provided"))
        return await repo.get_eff_by_week(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/test")
async def test():
    return {"test": "test"}


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
