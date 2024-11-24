from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm.scoping import ScopedSession

from core.data.models.user_model import UserModel
from core.data.repositories.userRepo import UserRepository
from core.data.schemas import user_schema
from core.db.database import get_scoped_db_session
from core.data.models import user_model
from core.security.auth import get_user_by_token, has_permission, get_user_by_basic, has_role_permission

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# Dependency to get the repository
def get_user_repository(db : ScopedSession = Depends(get_scoped_db_session)):
    return UserRepository(db)


@router.get("/", response_model=List[UserModel])
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db = Depends(get_scoped_db_session),
        current_user: user_model = Depends(get_user_by_token)
):
    if not has_permission(current_user, "read"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.query(user_schema.UserSchema).offset(skip).limit(limit).all()

    return users


@router.get("/get_all", response_model=List[UserModel])
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db = Depends(get_scoped_db_session),
        current_user: user_model.UserModel = Depends(get_user_by_basic)
):
    if not has_role_permission(current_user, ["admin", "user"]):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not has_permission(current_user, "read"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.query(user_schema.UserSchema).offset(skip).limit(limit).all()

    return users


@router.post("/create")
async def create_user(
        user: user_model.CreateUserModel,
        repo: UserRepository = Depends(get_user_repository),
):

    try:
        _result = repo.create_user(user)

        return {"message": "User created successfully", "user": _result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



