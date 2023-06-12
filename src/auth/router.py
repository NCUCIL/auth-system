import os

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import service

from ..modules.jwt import JWT
from .. import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get(
    "/callBack",
    responses={
        status.HTTP_302_FOUND: {
            "description": "User token created, redirect to where you were",
        }
    },
    status_code=status.HTTP_302_FOUND
)
async def auth_callBack(code, state, db: Session = Depends(get_db)):

    token = await service.get_token(code)
    
    if token == None:
        raise HTTPException(500, "NCU Oauth2 Failed Requesting access token")
    
    info = await service.get_info(token)

    if info == None:
        raise HTTPException(500, "NCU Oauth2 Failed Requesting user info")
    
    jwt = JWT()
    uid = service.ensure_user_existance(db, info.get("identifier"), info.get("chineseName"))
    token = jwt.generate(uid)

    response = RedirectResponse(state)
    response.set_cookie(key="token", value=token, expires=int(os.getenv("JWT_EXPIRE_TIME")))

    return response