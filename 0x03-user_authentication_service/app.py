#!/usr/bin/env python3
"""
Flask App Module
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def flask_app():
    """
    Basic Flask App
    Retruns:
        {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    Register User EndPoint
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return (jsonify({"email": user.email, "message": "user created"}))
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    Login a User Based on User SessionID
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if (not AUTH.valid_login(email, password)):
        abort(401)

    session_id = AUTH.create_session(email)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)