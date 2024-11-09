#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash the password using bcrypt """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return (hashed_password)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Implement is_valid to validate provided password
    matched hashed_password
    """
    encode = password.encode('utf-8')
    check_passwd = bcrypt.checkpw(encode, hashed_password)

    return (check_passwd)
