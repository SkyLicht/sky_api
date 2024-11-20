from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from core.data.models import user_model
from core.db.database import get_db_session
from core.schema import user_schema
from core.security.auth import get_user_by_token, has_permission, get_user_by_basic

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=List[user_schema.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session),
    current_user: user_model.User = Depends(get_user_by_token)
):

    if not has_permission(current_user, "read"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.query(user_model.User).offset(skip).limit(limit).all()
    return users


@router.get("/get_basic", response_model=List[user_schema.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session),
    current_user: user_model.User = Depends(get_user_by_basic)
):

    if not has_permission(current_user, "read"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.query(user_model.User).offset(skip).limit(limit).all()
    return users