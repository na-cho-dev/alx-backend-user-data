#!/usr/bin/env python3
"""
SessionAuth Class Module
"""
from flask import request
from .auth import Auth


class SessionAuth(Auth):
    """
    Manage the API authentication using Session Authentication
    """
