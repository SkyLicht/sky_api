# app/auth.py
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials

from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from core.data.handlers.translator import translate_user_schema_to_model
from core.data.models.user_model import UserModel
from core.data.schemas.user_schema import UserSchema
from core.db.database import get_db_session
from core.data.models.token_model import TokenDataModel

# Secret key to encode JWT tokens
SECRET_KEY = "4f1dada27ca17e21e166dc7e7c8978e3d32d25832432b3fcde66e988c4c9de35"  # Replace with your own secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBasic()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> Optional[UserSchema]:
    return db.query(UserSchema).filter(UserSchema.username == username).first()


def get_user_by_basic(
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db_session)
)-> UserModel:
    user = get_user(db, credentials.username)
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return UserModel.model_validate(user)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Dependency to get the current active user
async def get_user_by_token(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataModel(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, token_data.username)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def get_user_permissions(user: UserModel):
    permissions = set()
    for role in user.roles:
        for perm in role.permissions:
            permissions.add(perm.name)
    return permissions

def get_user_roles(user: UserModel):
    roles = set()
    for role in user.roles:
        roles.add(role.name)
    return roles


def has_permission(user: UserModel, permission_name: str):
    return permission_name in get_user_permissions(user)

def has_role_permission(user: UserModel, role_name: list[str]):
    return any(role in get_user_roles(user) for role in role_name)

