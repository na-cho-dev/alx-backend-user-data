#!/usr/bin/env python3
"""
DB Module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User
from typing import Dict, Union

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """
    DB class
    """
    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Save the user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Dict[str, Union[str, int]]) -> User:
        """
        Returns the first row found in the users table as
        filtered by the method’s input arguments
        """
        for key, val in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError
            query = (self._session.query(User)
                     .filter(getattr(User, key) == val))

        # user_query = (self._session.query(User)
        #                 .filter(getattr(User, key) == val).first())

        user_query = query.first()
        if user_query is None:
            raise NoResultFound
        return user_query

    def update_user(self, user_id: int,
                    **kwargs: Dict[str, Union[str, int]]) -> None:
        """
        Use find_user_by to locate the user to update, then will
        update the user’s attributes as passed in the method’s arguments
        """
        user = self.find_user_by(id=user_id)

        for key, val in kwargs.items():
            if not hasattr(User, key):
                raise ValueError
            setattr(user, key, val)
        self._session.commit()
