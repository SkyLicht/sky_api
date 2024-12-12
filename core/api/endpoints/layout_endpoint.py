from fastapi import APIRouter, Depends, HTTPException

from core.data.dao.cycle_time.layout_dao import LayoutDAO
from core.data.repositories.cycle_time.layout_repository import LayoutRepository
from core.db.database import get_scoped_db_session

router = APIRouter(
    prefix="/layout",
    tags=["layout"],
)


def get_layout_repository(db=Depends(get_scoped_db_session)):
    return LayoutRepository(dao=LayoutDAO(db))


@router.get("/get_by_line")
async def get_layout_by_line_id(line_id: str, repo: LayoutRepository = Depends(get_layout_repository)):
    try:
        layout = await repo.get_layout_by_line_id(line_id)
        return layout
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
