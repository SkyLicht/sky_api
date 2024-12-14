from fastapi import APIRouter, Depends, HTTPException

from core.data.repositories.platform_repository import PlatformRepository
from core.db.database import get_scoped_db_session

router = APIRouter(
    prefix="/platform",
    tags=["platform"]
)



def get_platform_repository(db = Depends(get_scoped_db_session)):
    return PlatformRepository(db)


@router.get("/get_all")
async def get_platforms(repository: PlatformRepository = Depends(get_platform_repository)):
    try:
        platforms = await repository.get_platforms()

        if not platforms:
            return []
        return platforms

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))