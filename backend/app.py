"""
PartSelect Multi-Agent Chat Application.

A Flask-based web application that provides an intelligent chat interface
for PartSelect customers, utilizing multiple specialized agents for product
search, installation guidance, and customer support.

This module serves as the main entry point for the backend API, handling
authentication, session management, and message routing to appropriate agents.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from flask import Flask, jsonify, request
from flask_cors import CORS

from orchestrator import Orchestrator
from auth import (
    create_user,
    authenticate_user,
    create_token,
    verify_token,
)


app = Flask(__name__)
CORS(app)
orchestrator = Orchestrator()

sessions: Dict[str, Dict[str, Any]] = {}


def _get_authenticated_user() -> Optional[str]:
    """
    Extract and verify the authenticated user from the request header.
    
    Returns
    -------
    Optional[str]
        The authenticated username if valid token is provided, None otherwise.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    return verify_token(token)


@app.route("/auth/register", methods=["POST"])
def register() -> Any:
    """
    Register a new user account.
    
    Expected JSON payload:
    {
        "username": "user123",
        "password": "password123"
    }
    
    Returns
    -------
    Any
        JSON response containing authentication token or error message.
    """
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400
    if not create_user(username, password):
        return jsonify({"error": "User already exists."}), 400
    token = create_token(username)
    return jsonify({"token": token})


@app.route("/auth/login", methods=["POST"])
def login() -> Any:
    """
    Authenticate an existing user.
    
    Expected JSON payload:
    {
        "username": "user123",
        "password": "password123"
    }
    
    Returns
    -------
    Any
        JSON response containing authentication token or error message.
    """
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400
    if not authenticate_user(username, password):
        return jsonify({"error": "Invalid username or password."}), 401
    token = create_token(username)
    return jsonify({"token": token})


@app.route("/chat", methods=["POST"])
def chat() -> Any:
    """
    Process a chat message and return an appropriate response.
    
    Requires authentication via Bearer token in Authorization header.
    
    Expected JSON payload:
    {
        "message": "How do I install this part?",
        "session_id": "unique-session-identifier"
    }
    
    Returns
    -------
    Any
        JSON response containing agent response, detected intent, and session info.
    """
    user = _get_authenticated_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True)
    message: str = data.get("message", "")
    session_id: str = data.get("session_id", "default")
    if not message:
        return jsonify({"error": "Missing 'message' field."}), 400
    
    session_key = f"{user}:{session_id}"
    context = sessions.setdefault(session_key, {})
    result = orchestrator.handle_message(message, context)
    
    return jsonify(
        {
            "response": result.get("response"),
            "agent": result.get("agent"),
            "intent": result.get("intent"),
            "session_id": session_id,
        }
    )


@app.route("/reset", methods=["POST"])
def reset() -> Any:
    """
    Reset the conversation context for a specific session.
    
    Requires authentication via Bearer token in Authorization header.
    
    Expected JSON payload:
    {
        "session_id": "unique-session-identifier"
    }
    
    Returns
    -------
    Any
        JSON response confirming the session reset.
    """
    user = _get_authenticated_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(force=True)
    session_id: str = data.get("session_id", "default")
    session_key = f"{user}:{session_id}"
    sessions.pop(session_key, None)
    return jsonify({"status": "reset", "session_id": session_id})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)