from typing import List
from pydantic import BaseModel

class PermissionBase(BaseModel):
    name: str
    description: str = ""

class UserBase(BaseModel):
    name: str

class UserPermissionsBase(BaseModel):
    pass


class PermissionCreate(PermissionBase):
    pass

class UserCreate(UserBase):
    ncu_id: str

class UserPermissionsCreate(UserPermissionsBase):
    uid: int
    pid: int

class PermissionOut(PermissionBase):

    class Config:
        orm_mode = True

class Permission(PermissionBase):
    users: list[UserBase] = []

    class Config:
        orm_mode = True

class User(UserBase):
    ncu_id: str
    permissions: List[PermissionOut] = []

    class Config:
        orm_mode = True