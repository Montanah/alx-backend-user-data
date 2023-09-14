#!/usr/bin/env python3
"""DB module"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method that saves the user to the database
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()

        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

        return new_user

	
    def find_user_by(self, **kwargs) -> User:
        """Method that returns the first row found in the users table
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is not None:
                return user
            else:
                return User(id=-1, email="", hashed_password="", session_id="",
                            reset_token="")
        except NoResultFound:
            return User(id=-1, email="", hashed_password="", session_id="",
                        reset_token="")
