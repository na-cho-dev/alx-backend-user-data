#!/usr/bin/env python3
"""
SessionDBAuth Module
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth Class
    """
    def create_session(self, user_id=None) -> str:
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

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Returns the User ID by requesting UserSession in the database
        based on session_id
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if len(sessions) <= 0:
            return None

        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None

        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the UserSession based on the Session ID from the
        request cookie
        """
        session_id = self.session_cookie(request)

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if len(sessions) <= 0:
            return False

        sessions[0].remove()
        return True
