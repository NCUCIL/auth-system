import os
import aiohttp
import base64

from sqlalchemy.orm import Session

from ..users.schemas import UserCreate
from ..users.service import get_user_by_ncu_id, create_user, get_user

async def async_post(url: str, **kwargs) -> dict:
    """Async post request

    Args:
        url (str): the url target

    Returns:
        json: json response of the request
    """

    async with aiohttp.ClientSession() as session:

        async def fetch(url):
            async with session.post(url, **kwargs) as response:
                return await response.json()
            
        return await fetch(url)
    
async def async_get(url: str, **kwargs) -> dict:
    """Async get request

    Args:
        url (str): The url target

    Returns:
        dict: json response
    """

    async with aiohttp.ClientSession() as session:

        async def fetch(url):
            async with session.get(url, **kwargs) as response:
                return await response.json()
            
        return await fetch(url)

async def get_token(code: str) -> str:
    """Get access token by the code recieved from NCU Portal

    Args:
        code (str): recieved code string

    Returns:
        str: user info returned by NCU Portal
    """

    client_id = os.getenv("PORTAL_OAUTH_ID")
    client_secret = os.getenv("PORTAL_OAUTH_SECRET")
    url = os.getenv("PORTAL_TOKEN_URL")

    basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')

    response = await async_post(url, data = {
        "grant_type": "authorization_code",
        "code": code,
    }, headers = {
        "Authorization": f"Basic {basic_auth}",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    })

    return response.get('access_token', None)

async def get_info(token: str) -> dict:
    """Get user info by the access token

    Args:
        token (str): access token

    Returns:
        dict: json response of user info
    """

    url = os.getenv("PORTAL_INFO_URL")

    try:
        response = await async_get(url, headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        })
    except Exception as e:
        print(f"ERROR:\tFetching user failed from NCU Oauth2 as {e}")
        return None

    return response

def ensure_user_existance(db: Session, ncu_id: str, name: str) -> int:
    """Make sure that the user exist in the database

    Args:
        db (Session): db connection
        ncu_id (str): user's ncu identifier
        name (str): user's chinese name

    Returns:
        int: user id
    """

    user = get_user_by_ncu_id(db, ncu_id)

    if user is not None:
        return user.id
    
    user = create_user(db, UserCreate(ncu_id=ncu_id, name=name))

    return user.id
