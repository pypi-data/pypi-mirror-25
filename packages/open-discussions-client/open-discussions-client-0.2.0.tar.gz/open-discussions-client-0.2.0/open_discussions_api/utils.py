"""API utils"""
import time

import jwt

EXPIRATION_DELTA_SECONDS = 60 * 60


def get_token(secret, username, roles, expires_delta=EXPIRATION_DELTA_SECONDS):
    """
    Gets a JWt token

    Args:
        username (str): user's username
        roles (list(str)): list of roles
        expires_delta (int): offset in second of token expiration

    Returns:
        str: encoded JWT token
    """
    now = int(time.time())
    return jwt.encode({
        'username': username,
        'roles': roles,
        'exp': now + expires_delta,
        'orig_iat': now,
    }, secret, algorithm='HS256').decode('utf-8')
