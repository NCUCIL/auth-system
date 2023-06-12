import pytest

from src.users.service import exist_user, get_user_info

USER1 = {
    "id": 12345,
    "name": "Test User",
    "ncu_id": "100000000",
    "is_valid": True
}
class MockService:

    def get_one_user(db, uid):
        user = USER1
        user["id"] = uid
        return user
    
    def get_no_user(db, uid):
        return None

@pytest.mark.parametrize("uid", [1])
def test_user_exist(db, uid, mocker):
    """REF.2.AS.7
    """

    mocker.patch("src.users.service.get_user", MockService.get_one_user)

    response = exist_user(db, uid)

    assert response == True

@pytest.mark.parametrize("uid", [2])
def test_user_not_exist(db, uid, mocker):
    """REF.2.AS.7
    """

    mocker.patch("src.users.service.get_user", MockService.get_no_user)

    response = exist_user(db, uid)

    assert response == False

def test_get_user_info(db, jwt_token: str, mocker):

    mocker.patch("src.modules.jwt.JWT.validate", return_value=12345)
    mocker.patch("src.users.service.get_user", MockService.get_one_user)
    
    response = get_user_info(db, jwt_token)

    assert response == USER1

def test_get_user_info_invalid(db, jwt_token, mocker):

    mocker.patch("src.modules.jwt.JWT.validate", return_value=-1)
    mocker.patch("src.users.service.get_user", MockService.get_one_user)
    
    response = get_user_info(db, jwt_token)

    assert response == None


