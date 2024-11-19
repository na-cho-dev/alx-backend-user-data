#!/usr/bin/env python3
"""
Hash Password Module
"""
import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hash a Password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed


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
        """
        Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new User
        """
        try:
            find_user = self._db.find_user_by(email=email)
            if find_user:
                raise ValueError("User {} already exists".format(email))
        except (NoResultFound, InvalidRequestError):
            hashed_password = _hash_password(password).decode('utf-8')
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check for Valid Login Details
        """
        try:
            find_user = self._db.find_user_by(email=email)
            hashed_password = find_user.hashed_password.encode('utf-8')
            password = password.encode('utf-8')
            return bcrypt.checkpw(password, hashed_password)
        except NoResultFound:
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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Find user by session ID
        """
        if not session_id:
            return None

        try:
            find_user = self._db.find_user_by(session_id=session_id)
            return find_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass
