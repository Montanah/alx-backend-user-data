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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Method that takes mandatory email and password string
        arguments and returns a User object
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            pass

        password = _hash_password(password)
        user = self._db.add_user(email, password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Method that takes email and password string arguments and returns
        a boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            return user and user.is_valid_password(password)
        except NoResultFound:
            return False
