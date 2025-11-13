from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol

try:
    from cryptography.fernet import Fernet
    CRYPTO_OK = True
except Exception:
    Fernet = None  # type: ignore
    CRYPTO_OK = False


class EncryptionStrategy(ABC):
    """GoF Strategy: interchangeable encryption algorithms."""

    @abstractmethod
    def encrypt(self, plaintext: str, *, user: str | None = None) -> bytes:
        ...

    @abstractmethod
    def decrypt(self, ciphertext: bytes, *, user: str | None = None) -> str:
        ...


class KeyProvider(Protocol):
    def get_key(self, user: str) -> bytes:  # raw key material; interpretation up to strategy
        ...


class NoOpStrategy(EncryptionStrategy):
    """No-op for testing. Do not use in production."""

    def encrypt(self, plaintext: str, *, user: str | None = None) -> bytes:
        return plaintext.encode("utf-8")

    def decrypt(self, ciphertext: bytes, *, user: str | None = None) -> str:
        return ciphertext.decode("utf-8")


class ReversibleStrategy(EncryptionStrategy):
    """Toy reversible algorithm (reverse string). Demonstration only."""

    def encrypt(self, plaintext: str, *, user: str | None = None) -> bytes:
        return plaintext[::-1].encode("utf-8")

    def decrypt(self, ciphertext: bytes, *, user: str | None = None) -> str:
        return ciphertext.decode("utf-8")[::-1]


class FernetStrategy(EncryptionStrategy):
    """Fernet-based strategy using a key per user (requires cryptography)."""

    def __init__(self, key_provider: KeyProvider):
        if not CRYPTO_OK:
            raise RuntimeError("cryptography not available for FernetStrategy")
        self._kp = key_provider

    def encrypt(self, plaintext: str, *, user: str | None = None) -> bytes:
        if not user:
            raise ValueError("user required for FernetStrategy")
        key = self._kp.get_key(user)
        f = Fernet(key)
        return f.encrypt(plaintext.encode("utf-8"))

    def decrypt(self, ciphertext: bytes, *, user: str | None = None) -> str:
        if not user:
            raise ValueError("user required for FernetStrategy")
        key = self._kp.get_key(user)
        f = Fernet(key)
        return f.decrypt(ciphertext).decode("utf-8")
