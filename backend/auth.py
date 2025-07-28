"""Simple JWT‑based authentication and user management.

This module provides helper functions for registering users, verifying
passwords and issuing/validating JSON Web Tokens (JWT). Passwords are
hashed using bcrypt. Tokens include the username and an expiration time.

Note: In a real application you would use a persistent database for
users and follow more robust security practices.
"""

from __future__ import annotations

import datetime
import os
from typing import Dict, Optional

import bcrypt
import jwt


JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", "86400"))

# In‑memory user store {username: password_hash}
USERS: Dict[str, bytes] = {}


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


def create_user(username: str, password: str) -> bool:
    if username in USERS:
        return False
    USERS[username] = hash_password(password)
    return True


def authenticate_user(username: str, password: str) -> bool:
    if username not in USERS:
        return False
    return verify_password(password, USERS[username])


def create_token(username: str) -> str:
    now = datetime.datetime.utcnow()
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None