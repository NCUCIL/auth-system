from pydantic import BaseModel

class PermissionBase(BaseModel):
    pass

class UserBase(BaseModel):
    name: str

class UserPermissionsBase(BaseModel):
    name: str
    descipriton: str = ""


class PermissionCreate(PermissionBase):
    pass

class UserCreate(UserBase):
    ncu_id: str

class UserPermissionsCreate(UserPermissionsBase):
    uid: int
    pid: int


class Permission(PermissionBase):
    pass
    users: list[UserBase] = []

    class Config:
        orm_mode = True

class User(UserBase):
    ncu_id: str
    permissions: list[UserPermissionsBase] = []

    class Config:
        orm_mode = True