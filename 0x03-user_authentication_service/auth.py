#!/usr/bin/env python3
""" Auth module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union
import bcrypt


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """ Method that takes in a password string arguments and returns
        bytes. The returned bytes is a salted hash of the input password,
        hashed with bcrypt.hashpw
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """ Method that takes mandatory email and password string
        arguments and returns a User object
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            pass

        hashed_password = self._hash_password(password)
        new_user = self._db.add_user(email, hashed_password)

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Method that takes email and password string arguments and returns
        a boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            return user and user.is_valid_password(password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Method that takes an email string argument and returns the session
        ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = str(uuid4())
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """ Method that takes a single session_id string argument and returns
        the corresponding User or None
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None

    def destroy_session(self, user_id: int) -> None:
        """ Method that takes a single user_id integer argument and returns
        None
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Method that takes an email string argument and returns a string
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = str(uuid4())
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Method that takes reset_token string argument and a password
        string argument and returns None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                password = _hash_password(password)
                self._db.update_user(user.id, password=password,
                                     reset_token=None)
        except NoResultFound:
            raise ValueError

    def __repr__(self) -> str:
        """Return string representation of the Auth instance."""
        return 'Auth()'
