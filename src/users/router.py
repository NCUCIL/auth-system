from fastapi import APIRouter, status, Response, Depends
from sqlalchemy.orm import Session

from .. import get_db
from . import schemas, service

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
    },
)
async def read_users_me(response: Response):
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"detail": "User Not Found"}

# TODO Temp endpoint for testing user creations
@router.get("/create")
async def create_users(db: Session = Depends(get_db)):

    new_user = schemas.UserCreate(**{"name":"Test User", "ncu_id":"100000000", "is_active": True})
    return service.create_user(db, new_user)

# TODO Temp endpoint for testing user 
@router.get("/{uid}", response_model=schemas.User)
async def read_users(uid: int, db: Session = Depends(get_db)):

    return service.exist_user(db, uid)
