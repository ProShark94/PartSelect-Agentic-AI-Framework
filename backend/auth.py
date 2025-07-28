"""
JWT-Based Authentication System.

This module provides a lightweight authentication system using JSON Web Tokens
(JWT) for secure user management in the PartSelect chat application. It includes
user registration, password hashing with bcrypt, and token-based authentication.

Security Features:
- Password hashing using bcrypt with salt
- JWT tokens with configurable expiration
- Secure token validation and verification

Note
----
This implementation uses in-memory storage for demonstration purposes.
Production deployments should integrate with a persistent database system.
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

USERS: Dict[str, bytes] = {}


def hash_password(password: str) -> bytes:
    """
    Generate a secure hash for the given password.
    
    Parameters
    ----------
    password : str
        The plain text password to hash.
    
    Returns
    -------
    bytes
        The bcrypt hashed password with salt.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    """
    Verify a password against its stored hash.
    
    Parameters
    ----------
    password : str
        The plain text password to verify.
    hashed : bytes
        The stored bcrypt hash to compare against.
    
    Returns
    -------
    bool
        True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


def create_user(username: str, password: str) -> bool:
    """
    Register a new user account.
    
    Parameters
    ----------
    username : str
        The desired username for the new account.
    password : str
        The plain text password for the new account.
    
    Returns
    -------
    bool
        True if the user was created successfully, False if username exists.
    """
    if username in USERS:
        return False
    USERS[username] = hash_password(password)
    return True


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user with username and password.
    
    Parameters
    ----------
    username : str
        The username to authenticate.
    password : str
        The plain text password to verify.
    
    Returns
    -------
    bool
        True if authentication succeeds, False otherwise.
    """
    if username not in USERS:
        return False
    return verify_password(password, USERS[username])


def create_token(username: str) -> str:
    """
    Generate a JWT token for an authenticated user.
    
    Parameters
    ----------
    username : str
        The username to encode in the token.
    
    Returns
    -------
    str
        A signed JWT token with expiration timestamp.
    """
    now = datetime.datetime.utcnow()
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[str]:
    """
    Validate a JWT token and extract the username.
    
    Parameters
    ----------
    token : str
        The JWT token to validate.
    
    Returns
    -------
    Optional[str]
        The username if the token is valid, None if expired or invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None