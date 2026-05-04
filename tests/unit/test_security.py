import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


def test_password_hash_and_verify():
    plain = "supersecret"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrong", hashed)


def test_token_roundtrip():
    token = create_access_token(subject="user-123")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-123"


def test_invalid_token_raises():
    with pytest.raises(ValueError):
        decode_access_token("not.a.valid.token")
