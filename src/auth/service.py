import os
import aiohttp
import base64

async def async_post(url, **kwargs):

    async with aiohttp.ClientSession() as session:

        async def fetch(url):
            async with session.post(url, **kwargs) as response:
                return await response.json()
            
        return await fetch(url)
    
async def async_get(url, **kwargs):

    async with aiohttp.ClientSession() as session:

        async def fetch(url):
            async with session.get(url, **kwargs) as response:
                return await response.json()
            
        return await fetch(url)

async def get_token(code: str):

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

async def get_info(token: str):

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