#!/usr/bin/env python3
"""
Auth Class Module
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth():
    """
    Manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False - path and excluded_paths
        """
        if (path is None):
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns None - request will be the Flask request object
        """
        if (request is None):
            return None

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None - request will be the Flask request object
        """
        return None
