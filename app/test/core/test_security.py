from datetime import timedelta

from app.core.security import create_access_token, get_password_hash, verify_password


def test_create_access_token_success():
    # given
    subject = "test"
    expires_delta = timedelta(minutes=5)

    # when
    token = create_access_token(subject=subject, expires_delta=expires_delta)

    # then
    assert isinstance(token, str)
    assert token != ""


def tset_get_passwrod_hash_success():
    # given
    password = "test"

    # when
    hashed_password = get_password_hash(password)

    # then
    assert isinstance(hashed_password, str)
    assert hashed_password != ""
    assert hashed_password != password


def test_vetify_password_success():
    # given
    plain_password = "test"
    hashed_password = get_password_hash(plain_password)

    # when
    result = verify_password(
        plain_password=plain_password, hashed_password=hashed_password
    )

    # then
    assert result is True
    assert plain_password != hashed_password


def test_return_false_when_verify_password_with_wrong_password():
    # given
    plain_password = "test"
    hashed_password = get_password_hash(plain_password)
    another_plain_password = "test2"

    # when
    result = verify_password(
        plain_password=another_plain_password, hashed_password=hashed_password
    )

    # then
    assert result is False
