import sqlite3
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os

def get_user_key(username):
    """Fetch user’s salt from DB and generate AES key using PBKDF2."""
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise ValueError("User not found.")

    password_hash, salt = result
    salt_bytes = salt.encode()
    password_bytes = password_hash.encode()

    # Derive a 32-byte key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return Fernet(key)

def encrypt_data(plaintext: str, username: str) -> bytes:
    fernet = get_user_key(username)
    return fernet.encrypt(plaintext.encode())

def decrypt_data(ciphertext: bytes, username: str) -> str:
    fernet = get_user_key(username)
    return fernet.decrypt(ciphertext).decode()

def encrypt_data(plaintext: str, filepath: str, username: str):
    """
    Encrypts plaintext and writes to file at filepath using user's key.
    """
    fernet = get_user_key(username)
    ciphertext = fernet.encrypt(plaintext.encode())
    with open(filepath, "wb") as f:
        f.write(ciphertext)

def decrypt_data(filepath: str, username: str) -> str:
    """
    Reads ciphertext from file at filepath and decrypts using user's key.
    """
    fernet = get_user_key(username)
    with open(filepath, "rb") as f:
        ciphertext = f.read()
    return fernet.decrypt(ciphertext).decode()
