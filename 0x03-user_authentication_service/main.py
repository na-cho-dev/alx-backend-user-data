#!/usr/bin/env python3
"""
End-to-end Integration Test
"""
import requests


BASE_URL = "http://0.0.0.0:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    Registers a new User
    """
    url = f"{BASE_URL}/users"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    res_msg = {"email": email, "message": "user created"}

    assert response.status_code == 200, response.text
    assert response.json() == res_msg


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Login with an (Incorrect) email and password
    """
    url = f"{BASE_URL}/sessions"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Login with a (Correct) email and password
    """
    url = f"{BASE_URL}/sessions"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    res_msg = {"email": email, "message": "logged in"}

    # print(f"Status Code: {response.status_code}")
    assert response.status_code == 200
    assert response.json() == res_msg

    session_id = response.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """
    Access the profile page without logging in.
    """
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": ""}
    response = requests.get(url, cookies=cookies)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Access the profile page with the specified session ID.
    """
    url = f"{BASE_URL}/profile"
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    res_msg = {"email": EMAIL}

    assert response.status_code == 200
    assert response.json() == res_msg


def log_out(session_id: str) -> None:
    """
    Log out using the specified session ID.
    """
    url = f"{BASE_URL}/sessions"
    headers = {"Content-Type": "application/json"}
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    res_msg = {"message": "Bienvenue"}

    assert response.status_code == 200
    assert response.json() == res_msg


def reset_password_token(email: str) -> str:
    """
    Generate a reset password token
    """
    url = f"{BASE_URL}/reset_password"
    data = {'email': email}
    response = requests.post(url, data=data)

    assert response.status_code == 200

    reset_token = response.json()["reset_token"]
    res_msg = {"email": email, "reset_token": reset_token}

    assert response.json() == res_msg
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update User's password
    """
    url = f"{BASE_URL}/reset_password"
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put(url, data=data)
    res_msg = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == res_msg


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
