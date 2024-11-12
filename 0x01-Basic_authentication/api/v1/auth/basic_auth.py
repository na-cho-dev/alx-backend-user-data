#!/usr/bin/env python3
"""
Basic Auth Class Module
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Manage Basic Auth API authentication
    """
