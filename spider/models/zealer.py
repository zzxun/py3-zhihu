#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/17

""" Description: a dic
"""

from sqlalchemy import Column, Integer, DateTime, Sequence, String
from sqlalchemy.sql.expression import text
from .base import *


class Zealer(Base):
    __tablename__ = 'zealer'

    # zhihu id
    id = Column(Integer, Sequence('topic_associate_id_seq'), primary_key=True)
    tag = Column(String(100), unique=True, nullable=False)
    tid = Column(Integer)

    answer_id = Column(Integer, index=True, nullable=False)
    author_id = Column(Integer, index=True, nullable=False, server_default=text('0'))

    upvote_num = Column(Integer)

    creation_time = Column(DateTime, nullable=False, server_default=text('NOW()'))
    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))
