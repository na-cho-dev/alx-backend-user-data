#!/usr/bin/env python3
"""
Basic Auth Class Module
"""
from flask import request
from typing import List, TypeVar
from .auth import Auth
import base64
from models.user import User
import re


class BasicAuth(Auth):
    """
    Manage Basic Auth API authentication
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication:
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith("Basic ")):
            return None

        return (authorization_header[len("Basic "):])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None

        try:
            decoded = base64.b64decode(
                base64_authorization_header, validate=True).decode('utf-8')
            return decoded
        except (base64.binascii.Error, ValueError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        # if (decoded_base64_authorization_header is None or
        #         not isinstance(decoded_base64_authorization_header, str) or
        #         ":" not in decoded_base64_authorization_header):
        #     return (None, None)

        # username = decoded_base64_authorization_header.split(":")[0]
        # password = decoded_base64_authorization_header.split(":")[1]

        # return (username, password)
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request:
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        if not b64_auth_token:
            return None

        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        if not auth_token:
            return None

        email, password = self.extract_user_credentials(auth_token)
        if not email or not password:
            return None

        user = self.user_object_from_credentials(email, password)
        if not user:
            return None

        return user
