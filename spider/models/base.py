#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/15

""" Description: base model of sqlalchemy
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text

# base model
Base = declarative_base()


def updated(instance):
    instance.updated_at = text('NOW()')


def auto_session(func):
    """
    :param func: function run on session
    :return: decorate
    """

    def wrapper(*args, **kwargs):
        """:use scoped_session to run func, func's args[1] = session, auto commit and remove
           auto rollback
        :param args: *args, args[0] is @classmethod cls
        :param kwargs: **kwargs
        :return: func run result
        """
        session = args[1]
        result = None
        try:
            result = func(*args, **kwargs)
            session.commit()
        finally:
            session.rollback()

        return result

    return wrapper
