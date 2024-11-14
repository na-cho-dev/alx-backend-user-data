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

        user_info = self.user_id_by_session_id.get(session_id)
        if user_info is None:
            return None

        if "created_at" not in user_info.keys():
            return None

        if self.session_duration <= 0:
            return user_info.get("user_id")

        created_at = user_info.get("created_at")
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_info.get("user_id")
