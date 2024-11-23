# from pydantic import BaseModel
# from typing import List, Optional
#
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
# class User(UserBase):
#     id: int
#     is_active: bool
#     roles: List[Role] = []
#
