import base64
import json
from freezegun import freeze_time
from datetime import datetime, timedelta

from src.modules.jwt import JWT 

jwt = JWT()
jwt.secret = "DEFAULT_SECRET_IS_32_BIT_LENGTH!"

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

@freeze_time("2023-06-12T10:21:55+08:00")
def test_jwt_encode():
    """Check REF.2.AS.4, REF.2.AS.2
    """

    response = jwt.generate(12345)

    data: dict = json.loads(base64.b64decode(response.split('.')[1]).decode('utf-8'))

    assert data.get('uid') == 12345, "Check uid is in the jwt token"
    assert data.get('exp') == int((datetime.utcnow() + timedelta(hours=3)).timestamp()), "Check that jwt expires in 3 hours"
    assert response == FAKE_JWT

@freeze_time("2023-06-12T11:21:55+08:00")
def test_jwt_validation_valid():
    """Check REF.2.AS.5
    """

    response = jwt.validate(FAKE_JWT)

    assert response == 12345, "Check that jwt can be successfully decoded"

@freeze_time("2023-06-12T13:21:56+08:00")
def test_jwt_validation_invalid():
    """Check REF.2.AS.6
    """

    response = jwt.validate(FAKE_JWT)

    assert response == -1, "Check that returns -1 while jwt decode expires"