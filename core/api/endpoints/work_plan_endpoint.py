from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette.responses import JSONResponse
from core.api.handlers.work_plan_handler import handle_both_dates, handle_end_date_only, handle_line_only, \
    handle_start_date_only

from core.api.querys.work_plna_query import WorkPlanQuery
from core.data.models.hour_by_hour_model import WorkPlanModel
from core.data.repositories.work_plan_repository import WorkPlanRepository
from core.db.database import get_scoped_db_session

router = APIRouter(
    prefix="/work_plan",
    tags=["work_plan"]
)


def get_work_plan_repository(db=Depends(get_scoped_db_session)):
    return WorkPlanRepository(db)


@router.get("/get")
async def get_work_plan(query: WorkPlanQuery = Depends()):
    if query.start_date and query.end_date:
        result = await handle_both_dates(query)
    elif query.start_date and not query.end_date:
        result = await handle_start_date_only(query)
    elif query.end_date and not query.start_date:
        result = await handle_end_date_only(query)
    elif query.line and not query.start_date and not query.end_date:
        result = await handle_line_only(query)
    else:
        raise HTTPException(status_code=400, detail="At least one date parameter or line is required.")

    return result

    # """
    # Get work plan data for a specific line and date range.
    #
    # Args:
    #     line (str): The line name.
    #     start_date (str): The start date in 'yyyy-mm-dd' format.
    #     end_date (str): The end date in 'yyyy-mm-dd' format.
    #     factory (str): The factory name.
    #
    # Returns:
    #     JSONResponse: The work plan data as a JSON response.
    # """
    # # start_date_obj, end_date_obj = validate_date_range(start_date, end_date)
    # # work_plan_data = WorkPlanRepository(db).get_work_plan(line, start_date_obj, end_date_obj, factory)
    # # return JSONResponse(content=work_plan_data)
    # return JSONResponse(content={"message": "Work plan data"})


@router.post("/create")
async def create_work_plan(work_plan: WorkPlanModel,
                           repository: WorkPlanRepository = Depends(get_work_plan_repository)):

    try:
        respond = repository.create_work_plan(work_plan)
        return respond
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))