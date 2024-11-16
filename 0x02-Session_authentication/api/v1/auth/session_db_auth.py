#!/usr/bin/env python3
"""
SessionDBAuth Module
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth Class
    """
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession
        and returns the Session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {'user_id': user_id, 'session_id': session_id}
        # Creates and Stores a new instance of UserSession
        user_session = UserSession(**session_dict)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession in the database
        based on session_id
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return None

        if not user_session:
            return None

        user_data = user_session[0]

        if self.session_duration <= 0:
            return user_data.user_id

        created_at = user_data.created_at
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time > datetime.now():
            return None

        return user_data.user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID from the
        request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            UserSession.save()
            return True

        return False
