#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/17

""" Description: a dic
"""

from sqlalchemy import Column, Integer, DateTime, Sequence, String, Text, UniqueConstraint
from .base import *


class News(Base):
    __tablename__ = 'news'
    __table_args__ = (
        UniqueConstraint('tag', 'url', name='IDX_TAG_URL'),
    )

    id = Column(Integer, Sequence('news_id_seq'), primary_key=True)
    source = Column(String(10), nullable=False)
    tag = Column(String(20), nullable=False, server_default='')

    url = Column(String(100), nullable=False, server_default='')
    title = Column(String(200), nullable=False)

    image = Column(String(250))
    summary = Column(Text)

    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))

    @classmethod
    def create(cls, session, instance):
        session.add(instance)
