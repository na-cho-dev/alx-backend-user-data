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
        if not isinstance(email, str) or not isinstance(password, str):
            raise ValueError("Email and Password must be a string")

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check for Valid Login Details
        """
        try:
            find_user = self._db.find_user_by(email=email)
            password = password.encode('utf-8')
            hashed_password = (
                find_user.hashed_password.encode('utf-8')
                if isinstance(find_user.hashed_password, str)
                else find_user.hashed_password
            )
            # hashed_password = find_user.hashed_password.encode('utf-8')
            return bcrypt.checkpw(password, hashed_password)
        except Exception:
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

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a Reset Password Token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_tok = _generate_uuid()
            user.reset_token = reset_tok
            self._db._session.commit()
            return reset_tok
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates Users Password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            self._db._session.commit()
        except NoResultFound:
            raise ValueError
