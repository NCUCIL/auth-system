import base64
import json
from freezegun import freeze_time
from datetime import datetime, timedelta

@freeze_time("2023-06-12T10:21:55+08:00")
def test_jwt_encode(jwt, jwt_token):
    """Check REF.2.AS.4
    """

    response = jwt.generate(12345)

    data: dict = json.loads(base64.b64decode(response.split('.')[1]).decode('utf-8'))

    assert data.get('uid') == 12345, "Check uid is in the jwt token"
    assert data.get('exp') == int((datetime.utcnow() + timedelta(hours=3)).timestamp()), "Check that jwt expires in 3 hours"
    assert response == jwt_token

@freeze_time("2023-06-12T11:21:55+08:00")
def test_jwt_validation_valid(jwt, jwt_token):
    """Check REF.2.AS.5
    """

    response = jwt.validate(jwt_token)

    assert response == 12345, "Check that jwt can be successfully decoded"

@freeze_time("2023-06-12T13:21:56+08:00")
def test_jwt_validation_invalid(jwt, jwt_token):
    """Check REF.2.AS.6
    """

    response = jwt.validate(jwt_token)

    assert response == -1, "Check that returns -1 while jwt decode expires"