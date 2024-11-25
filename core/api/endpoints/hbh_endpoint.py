from fastapi import APIRouter, Depends, HTTPException

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
