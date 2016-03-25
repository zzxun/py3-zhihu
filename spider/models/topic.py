#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/17

""" Description: a dic
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql.expression import text
from .base import Base, updated
from datetime import datetime


class Topic(Base):
    __tablename__ = 'topic'

    # zhihu id
    id = Column(Integer, primary_key=True)
    # zhihu inner id
    tid = Column(Integer)

    url = Column(String(100), unique=True, nullable=False)
    photo_url = Column(String(100))

    name = Column(String(100), nullable=False)
    description = Column(Text)
    follower_num = Column(Integer, nullable=False, server_default=text('0'))

    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))
    updated_at = Column(DateTime, nullable=False, server_default=text('NOW()'),
                        onupdate=datetime.now)

    @classmethod
    def create_or_update(cls, session, instance):
        topic = session.query(Topic).filter(Topic.id == instance.id).one_or_none()

        if topic:
            topic.photo_url = instance.photo_url
            topic.description = instance.description
            topic.follower_num = instance.follower_num
            updated(topic)
        else:
            session.add(instance)
