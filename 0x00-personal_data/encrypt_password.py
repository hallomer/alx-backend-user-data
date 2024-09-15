#!/usr/bin/env python3
"""
Password Encryption Module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a hashed password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
