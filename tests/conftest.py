import os
import pytest

os.environ["STAGE"] = "TEST"

from src import get_db
from src.main import app
from src.database import SessionLocal

def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def db():
    return get_db()

from src.modules.jwt import JWT 

mock_jwt = JWT()
mock_jwt.secret = "DEFAULT_SECRET_IS_32_BIT_LENGTH!"

FAKE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEyMzQ1LCJleHAiOjE2ODY1NDczMTV9.N_4XS-NDxTGgIRRYWlUVsKR3GXCl-oGFYQ3_kKk_nQg"
""" 
{
  "alg": "HS256",
  "typ": "JWT",
}
{
  "uid": 12345,
  "exp": 1686547315 # 2023-06-12T13:21:55+08:00
}
"""

@pytest.fixture
def jwt() -> JWT:
    return mock_jwt

@pytest.fixture
def jwt_token() -> str:
    return FAKE_JWT