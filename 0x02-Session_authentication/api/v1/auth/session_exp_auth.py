#!/usr/bin/env python3
""" Session Expiration Authentication
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Expiration authentication class
    """
    def __init__(self):
        """ Initialize the SessionExpAuth instance
        """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a session ID with an expiration date
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get user_id from session id
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        if (created_at + timedelta(seconds=self.session_duration) <
                datetime.now()):
            return None
        return session_dict.get('user_id')
