#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates and returns a new UUID as a string
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the provided email and password
        """
        try:
            user = self._db.find_user_by(email=email)
            is_valid_password = bcrypt.checkpw(password.encode(),
                                               user.hashed_password)
            return is_valid_password
        except NoResultFound:
            return False

    def create_session(self, email: str = None) -> str:
        """Creates a new session for a user and returns the session ID
        """
        if email is None:
            return None
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str = None) -> str:
        """Find a user by their session ID
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int = None) -> None:
        """Destroy a user's session by updating their session ID to None
        """
        if user_id is None:
            return None

        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for a user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password with the provided reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
