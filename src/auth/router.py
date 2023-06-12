from fastapi import APIRouter, status, HTTPException

from .service import get_token, get_info

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get(
    "/callBack",
)
async def auth_callBack(code, state):

    token = await get_token(code)
    
    if token == None:
        raise HTTPException(500, "NCU Oauth2 Failed Requesting access token")
    
    info = await get_info(token)

    if info == None:
        raise HTTPException(500, "NCU Oauth2 Failed Requesting user info")

    return {
        "data": info
    }
