"""Tests for security utilities — hashing, tokens, encryption."""
import uuid

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    encrypt_credential,
    decrypt_credential,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        hashed = hash_password("my_password")
        assert hashed != "my_password"
        assert verify_password("my_password", hashed) is True

    def test_wrong_password(self):
        hashed = hash_password("correct")
        assert verify_password("wrong", hashed) is False

    def test_different_hashes(self):
        h1 = hash_password("same")
        h2 = hash_password("same")
        assert h1 != h2  # Different salts


class TestTokens:
    def test_access_token_roundtrip(self):
        uid = uuid.uuid4()
        tid = uuid.uuid4()
        token = create_access_token(uid, tid, "client")
        payload = decode_token(token)
        assert payload["sub"] == str(uid)
        assert payload["tenant_id"] == str(tid)
        assert payload["role"] == "client"
        assert payload["type"] == "access"

    def test_refresh_token_roundtrip(self):
        uid = uuid.uuid4()
        token = create_refresh_token(uid)
        payload = decode_token(token)
        assert payload["sub"] == str(uid)
        assert payload["type"] == "refresh"

    def test_invalid_token_raises(self):
        import pytest
        with pytest.raises(ValueError, match="Invalid token"):
            decode_token("garbage.token.here")


class TestEncryption:
    def test_encrypt_decrypt_roundtrip(self):
        plaintext = "super_secret_wifi_password"
        encrypted = encrypt_credential(plaintext)
        assert encrypted != plaintext
        decrypted = decrypt_credential(encrypted)
        assert decrypted == plaintext
