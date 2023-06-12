from sqlalchemy.orm import Session

from . import models, schemas
from ..modules.jwt import JWT

jwt = JWT()

def get_user(db: Session, uid: int) -> models.Users:

    return db.query(models.Users).filter(models.Users.id == uid).first()

def exist_user(db: Session, uid: int) -> bool:
    return False if get_user(db, uid) == None else True

def get_user_info(db: Session, jwt_token: str) -> models.Users:

    result = jwt.validate(jwt_token)

    if result == -1:
        return None

    return get_user(db, result)

def create_user(db: Session, user: schemas.UserCreate) -> models.Users:

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user