from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ncu_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    permissions = relationship("Permissions", secondary="user_permissions", back_populates="users")


class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, default="")

    users = relationship("Users", secondary="user_permissions", back_populates="permissions")

class UserPermissions(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer, ForeignKey("users.id"))
    pid = Column(Integer, ForeignKey("permissions.id") )
