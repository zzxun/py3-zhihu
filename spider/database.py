#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gmail.com>
# date:  2016/03/14
#

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from .models import *
from .config import *

_engine = create_engine(URL(drivername='mysql+' + MYSQL['driver'],
                            username=MYSQL['username'],
                            password=MYSQL['password'],
                            host=MYSQL['host'],
                            port=MYSQL['port'],
                            database=MYSQL['database'],
                            query={'charset': 'utf8mb4'}), echo=False)
SessionFactory = sessionmaker(bind=_engine)
Session = scoped_session(SessionFactory)

# initial db
Base.metadata.create_all(_engine)
print('connect to mysql')


def auto_session_except(func, *args, **kwargs):
    """:use scoped_session to run func, func's args[0] = session, auto commit and remove
    :param func: function run on session
    :param args: *args
    :param kwargs: **kwargs
    :return: func run result
    """
    session = Session()
    result = None
    try:
        result = func(*((session,) + args), **kwargs)
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.rollback()

    return result
