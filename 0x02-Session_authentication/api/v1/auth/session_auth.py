#!/usr/bin/env python3
"""
SessionAuth Class Module
"""
from flask import request
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    Manage the API authentication using Session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
