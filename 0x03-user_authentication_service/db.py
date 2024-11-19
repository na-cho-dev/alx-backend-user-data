#!/usr/bin/env python3
"""
DB Module
"""
from sqlalchemy import create_engine, tuple_
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
        attrs, vals = [], []
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise InvalidRequestError()
            attrs.append(getattr(User, attr))
            vals.append(val)

        session = self._session
        query = session.query(User)
        user = query.filter(tuple_(*attrs).in_([tuple(vals)])).first()
        if not user:
            raise NoResultFound()
        return user
        # try:
        #     user = self._session.query(User).filter_by(**kwargs).one()
        # except NoResultFound:
        #     raise NoResultFound()
        # except InvalidRequestError:
        #     raise InvalidRequestError()
        # return user
        # query = self._session.query(User)
        # for key, val in kwargs.items():
        #     if not hasattr(User, key):
        #         raise InvalidRequestError
        #     query = query.filter(getattr(User, key) == val)

        # user_query = query.first()
        # if user_query is None:
        #     raise NoResultFound
        # return user_query

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
