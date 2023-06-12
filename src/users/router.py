from fastapi import APIRouter, status, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from .. import get_db
from ..modules.jwt import JWT
from . import schemas
from ..users.service import get_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example":{
                        "detail": "User not found",
                    },
                },
            },
        },
    }
)

@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    description="Get user information",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.User,
            "description": "Success query",
            "content": {
                "application/json": {
                    "example":{
                        "name": "Example",
                        "ncu_id": "100000000",
                        "Permissions": [],
                    },
                },
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Requested with invalid auth type",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Only Bearer is permitted"
                    }
                }
            }
        },
    },
)
async def read_users_me(Authorization: str | None = Header(), db: Session = Depends(get_db)):

    if Authorization is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bearer authentication required")
    
    auth_type, token = Authorization.split(' ')

    if not auth_type == "Bearer":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Only Bearer is permitted")

    jwt = JWT()
    uid = jwt.validate(token)

    if uid == -1:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    user = get_user(db, uid)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user