#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/17

""" Description: a dic
"""

from sqlalchemy import Column, Integer, DateTime, BLOB
from sqlalchemy.sql.expression import text
from .base import *


class Comment(Base):
    __tablename__ = 'comment'

    # zhihu id
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)

    content = Column(BLOB)

    answer_id = Column(Integer, index=True, nullable=False)
    author_id = Column(Integer, index=True, nullable=False, server_default=text('0'))

    upvote_num = Column(Integer)

    creation_time = Column(DateTime, nullable=False, server_default=text('NOW()'))
    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))
