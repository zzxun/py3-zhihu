#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/19

""" Description: cookie of login user
"""

from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime
from sqlalchemy.sql.expression import text, update
from .base import Base
from ..common import encode_passwd
from datetime import datetime


class Cookie(Base):
    __tablename__ = 'cookie'

    id = Column(Integer, Sequence('cookie_id_seq'), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False, server_default='')
    cookie = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))
    updated_at = Column(DateTime, nullable=False, server_default=text('NOW()'),
                        onupdate=datetime.now)

    def __repr__(self):
        return "(id='%d', user='%s', createdAt='%s', updatedAt='%s', cookie='%s',)>" % \
               (self.id, self.username, self.createdAt, self.updatedAt, self.cookie)

    @classmethod
    def clean_cookies(cls, session, username):
        """ clean password and cookie for username
        :param session: db session
        :param username: Cookie.username
        """

        session.execute(update(Cookie).
                        where(Cookie.username == username).
                        values(password='', cookie='', updated_at=text('NOW()')))

    @classmethod
    def create_or_update(cls, session, username, password, cookies):
        """ add new or update exist
        :param username: email
        :param session: db session
        :param password: password origin
        :param cookies: zhihu cookies
        """
        cookie = session.query(Cookie). \
            filter(Cookie.username == username).one_or_none()

        password = encode_passwd(password)

        if cookie:
            cookie.password = password
            cookie.cookie = cookies
            cookie.updated_at = text('NOW()')
        else:
            cookie = Cookie(username=username, password=password, cookie=cookies)
            session.add(cookie)

    @classmethod
    def get_all_cookies(cls, session):
        """ show list of cookies by usernames
        :param session: db session
        :return: list of cookies
        """
        return session.query(Cookie).all()
