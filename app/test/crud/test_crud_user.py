import pytest
from sqlalchemy.orm import Session

from app.core.exception import ConflictException
from app.crud import crud_user
from app.schema.user import UserCreate


def test_get_by_tel_success(db: Session):
    # given
    data = {"tel": "01080007000", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when
    user = crud_user.get_by_tel(db=db, tel="01080007000")

    # then
    assert user is not None
    assert user.tel == "01080007000"
    assert user.id is not None


def test_get_by_tel_when_not_exists(db: Session):
    # when
    user = crud_user.get_by_tel(db=db, tel="01080007000")

    # then
    assert user is None


def test_create_success(db: Session):
    # given
    data = {"tel": "01011117777", "password": "1234"}

    # when
    user = crud_user.create(db=db, data=UserCreate(**data))

    # then
    assert user is not None
    assert user.tel == "01011117777"
    assert user.id is not None


def test_raise_conflict_exception_when_try_to_create_same_tel_user(db: Session):
    # given
    data = {"tel": "01011117777", "password": "1234"}
    user = crud_user.create(db=db, data=UserCreate(**data))

    # when, then
    same_tel_user_data = {"tel": "01011117777", "password": "1234"}
    with pytest.raises(ConflictException) as error_info:
        crud_user.create(db=db, data=UserCreate(**same_tel_user_data))
    assert error_info.value.args[0] == "'01011117777'는 이미 사용 중인 휴대폰 번호입니다."


def test_authenticate_success(db: Session):
    # given
    data = {"tel": "01022227777", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when
    user = crud_user.authenticate(db=db, tel="01022227777", password="1234")

    # then
    assert user is not None
    assert user.logout_flag is False
    assert user.tel == "01022227777"
    assert user.id is not None


def test_return_none_when_authenticate_with_not_exists_tel(db: Session):
    # given
    data = {"tel": "01022227777", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when
    user = crud_user.authenticate(db=db, tel="01012345678", password="1234")

    # then
    assert user is None


def test_return_none_when_authenticate_with_wrong_password(db: Session):
    # given
    data = {"tel": "01022227777", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when
    user = crud_user.authenticate(db=db, tel="01022227777", password="4321")

    # then
    assert user is None


def test_logout_success(db: Session):
    # given
    data = {"tel": "01033337777", "password": "1234"}
    crud_user.create(db=db, data=UserCreate(**data))
    user = crud_user.authenticate(db=db, tel="01033337777", password="1234")

    # when
    crud_user.logout(db=db, user=user)

    # then
    assert user is not None
    assert user.logout_flag is True
    assert user.tel == "01033337777"
    assert user.id is not None
