#!/usr/bin/env python3
""" Session Database Authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session Database Authentication class
    """
    def create_session(self, user_id=None):
        """ Create a session ID and store it in the UserSession
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get user_id from UserSession based on session_id
        """
        if session_id is None:
            return None
        user_sessions = UserSession.all()
        for user_session in user_sessions:
            if user_session.session_id == session_id:
                return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID from the cookie
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
