import pytest
from pytest_mock import MockerFixture

from src.auth.service import ensure_user_existance

from .conftest import MockService

class MockUser:

    ncu_id = "100000000"
    name = "Test User"

def test_ensure_user_when_exist(db, mocker: MockerFixture):
    """REF.2.AS.2
    """

    mocker.patch("src.auth.service.get_user_by_ncu_id", MockService.get_one_user)
    mock_create_user = mocker.patch("src.auth.service.create_user", autospec=True)
    
    response = ensure_user_existance(db, "100000000", "Test User")

    assert response == 12345
    mock_create_user.assert_not_called()

def test_ensure_user_when_exist(db, mocker: MockerFixture):
    """REF.2.AS.2
    """

    mocker.patch("src.auth.service.get_user_by_ncu_id", MockService.get_no_user)
    mocker.patch("src.auth.service.UserCreate", return_value=MockUser())
    mocker.patch("src.auth.service.create_user", MockService.create_user)

    response = ensure_user_existance(db, "100000000", "Test User")

    assert response == 12345
