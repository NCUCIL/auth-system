import pytest

from .conftest import MockService, user1

from src.users.service import exist_user, get_user_info

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
    """REF.2.AS.8
    """

    mocker.patch("src.modules.jwt.JWT.validate", return_value=12345)
    mocker.patch("src.users.service.get_user", MockService.get_one_user)
    
    response = get_user_info(db, jwt_token)

    assert response.id == user1.get("id")
    assert response.ncu_id == user1.get("ncu_id")
    assert response.name == user1.get("name")

def test_get_user_info_invalid(db, jwt_token, mocker):
    """REF.2.AS.8
    """
    
    mocker.patch("src.modules.jwt.JWT.validate", return_value=-1)
    mocker.patch("src.users.service.get_user", MockService.get_one_user)
    
    response = get_user_info(db, jwt_token)

    assert response == None


