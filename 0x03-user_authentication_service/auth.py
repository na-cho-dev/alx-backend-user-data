#!/usr/bin/env python3
"""
Hash Password Module
"""
import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    Hash a Password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def _generate_uuid() -> str:
    """
    Generate UUID
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password) -> User:
        """
        Registers a User
        """
        db = self._db
        try:
            find_user = db.find_user_by(email=email)
            if find_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check for Valid Login Details
        """
        try:
            find_user = self._db.find_user_by(email=email)
            if find_user:
                if (bcrypt.checkpw(password.encode('utf-8'),
                                   find_user.hashed_password)):
                    return True
        except NoResultFound:
            pass

        return False

    def create_session(self, email: str) -> str:
        """
        Generate a Session ID for user
        """
        try:
            find_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            find_user.session_id = session_id
            self._db._session.commit()

            return session_id
        except NoResultFound:
            return None