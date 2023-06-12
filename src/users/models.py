from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ncu_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    permission_relations = relationship("UserPermissions", back_populates="user")


class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, default="")

    permission_relations = relationship("UserPermissions", back_populates="permission")

class UserPermissions(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer, ForeignKey("users.id"))
    pid = Column(Integer, ForeignKey("permissions.id") )

    user = relationship("User", back_populates="permission_relations")
    permission = relationship("Permissions", back_populates="permission_relations")