#!/usr/bin/env python3
"""
End-to-end integration test for the User Authentication Service
"""
import requests

BASE_URL = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Register a new user
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/users", data=data)
    assert response.status_code == 200, (
        f"Register user failed with status code: {response.status_code}"
    )
    assert response.json() == {
        "email": email,
        "message": "user created"
    }


def log_in_wrong_password(email: str, password: str) -> None:
    """Try to log in with a wrong password
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=data)
    assert response.status_code == 401, (
        f"Log in with wrong password failed with status code: "
        f"{response.status_code}"
    )


def log_in(email: str, password: str) -> str:
    """Log in a user and return the session ID
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=data)
    assert response.status_code == 200, (
        f"Log in failed with status code: {response.status_code}"
    )
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Try to access the profile without being logged in
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, (
        f"Profile unlogged failed with status code: {response.status_code}"
    )


def profile_logged(session_id: str) -> None:
    """Access the profile while being logged in
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, (
        f"Profile logged failed with status code: {response.status_code}"
    )


def log_out(session_id: str) -> None:
    """Log out a user
    """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, (
        f"Log out failed with status code: {response.status_code}"
    )


def reset_password_token(email: str) -> str:
    """Request a password reset token
    """
    data = {"email": email}
    response = requests.post(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200, (
        f"Reset password token failed with status code: {response.status_code}"
    )
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password of a user
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200, (
        f"Update password failed with status code: {response.status_code}"
    )


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
