#!/usr/bin/env python3
"""
SessionExpAuth Class Module
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Manage SessionAuth Expiration
    """
    def __init__(self):
        """
        Initializes an Instance of SessionExpAuth
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session from SessionAuth
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a User ID based on a Session ID form SessionAuth
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id)

        if "created_at" not in self.user_id_by_session_id[session_id]:
            return None

        user_id = self.user_id_by_session_id[session_id]["user_id"]
        created_at = self.user_id_by_session_id[session_id]["created_at"]
        session_duration = self.session_duration
        expiration_time = created_at + timedelta(seconds=session_duration)

        if expiration_time < datetime.now():
            return None

        return user_id
