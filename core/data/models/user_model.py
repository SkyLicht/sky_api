from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

# class PermissionBase(BaseModel):
#     name: str
#
# class PermissionCreate(PermissionBase):
#     pass
#
# class Permission(PermissionBase):
#     id: int
#
#
# class RoleBase(BaseModel):
#     name: str
#
# class RoleCreate(RoleBase):
#     permissions: List[int] = []
#
# class Role(RoleBase):
#     id: int
#     permissions: List[Permission] = []
#
#
# class UserBase(BaseModel):
#     username: str
#
# class UserCreate(UserBase):
#     password: str
#     roles: List[int] = []
#
# class UserModel(UserBase):
#     id: int
#     is_active: bool
#     roles: List[Role] = []
#
# Pydantic model for User





# Permission Model
class PermissionModel(BaseModel):
    id: Optional[str]
    name: str

    # Enable compatibility with SQLAlchemy ORM
    model_config = ConfigDict(from_attributes=True)

# Role Model
class RoleModel(BaseModel):
    id: Optional[str]
    name: str
    permissions: List[PermissionModel] = Field(default_factory=list)
    # Enable compatibility with SQLAlchemy ORM
    model_config = ConfigDict(from_attributes=True)


# Route Model
class RouteModel(BaseModel):
    id: Optional[str]
    path: str
    name: str
    description: Optional[str] = None

    # Enable compatibility with SQLAlchemy ORM
    model_config = ConfigDict(from_attributes=True)


# User Model
class UserModel(BaseModel):
    id: Optional[str]
    username: str
    is_active: bool
    roles: List[RoleModel] = Field(default_factory=list)   # List of Role models
    routes: List[RouteModel] = Field(default_factory=list)   # List of Route models

    # Enable compatibility with SQLAlchemy ORM
    model_config = ConfigDict(from_attributes=True)


# Create User Model
class CreateUserModel(BaseModel):
    username: str
    password: str
    role: str





