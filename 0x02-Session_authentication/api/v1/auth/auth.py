#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar
import fnmatch
from os import getenv


class Auth:
    """ Manages the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        path = path if path.endswith('/') else path + '/'
        for pattern in excluded_paths:
            if fnmatch.fnmatch(path, pattern):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Get the authorization header
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user
        """
        return None

    def session_cookie(self, request=None) -> str:
        """ Retrieve the session cookie value from the request
        """
        if request is None:
            return None
        session_name = getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
