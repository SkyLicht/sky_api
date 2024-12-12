from fastapi import APIRouter, Depends, HTTPException

from core.data.dao.line_dao import LineDAO
from core.data.repositories.line_repository import LineRepository
from core.db.database import get_scoped_db_session

router = APIRouter(
    prefix="/line",
    tags=["line"],
)


def get_line_repository(db=Depends(get_scoped_db_session)):
    return LineRepository(dao= LineDAO(db))


@router.get("/")
async def test():
    return {
        "message": "Hello World"
    }


@router.get("/get_all")
async def get_lines(repo: LineRepository = Depends(get_line_repository)):
    try:
        lines = await repo.get_lines()
        return lines
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
