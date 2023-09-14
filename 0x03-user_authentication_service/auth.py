#!/usr/bin/env python3
""" Auth module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> str:
    """ Method that takes in a password string arguments and returns
    bytes. The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
