#!/usr/bin/env python3
""" Session Authentication View
"""
from flask import jsonify, request
from models.user import User
from api.v1.app import auth
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /auth_session/login
    Logs in a user and creates a Session ID.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout() -> str:
    """ DELETE /auth_session/logout
    Logs out the user.
    """
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        return jsonify({"error": "Not found"}), 404
