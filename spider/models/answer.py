#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/17

""" Description: a dic
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql.expression import text, false
from .base import Base
from datetime import datetime

DEFAULT_TYPES = ['hot', 'top']
TYPES = DEFAULT_TYPES + ['all', 'tips']


class Answer(Base):
    __tablename__ = 'answer'

    # zhihu id
    id = Column(Integer, primary_key=True)
    aid = Column(Integer)

    url = Column(String(100), unique=True, nullable=False)
    content = Column(Text)

    question = Column(Integer, index=True, nullable=False)

    author_url = Column(String(100), nullable=False, server_default='')
    author = Column(String(100), nullable=False, server_default='')
    author_name = Column(String(100), nullable=False, server_default='')

    # 收藏, 评论, 赞
    collect_num = Column(Integer)
    comment_num = Column(Integer)
    upvote_num = Column(Integer)

    deleted = Column(Boolean, nullable=False, server_default=false())

    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))
    hot_updated_at = Column(DateTime)
    top_updated_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=False, server_default=text('NOW()'),
                        onupdate=datetime.now)

    @classmethod
    def create_or_update(cls, session, instance, update=None):
        """
        :param session: DB
        :param instance: new one
        :param update: if updated hot_updated_at / top_updated_at
        :return:
        """
        answer = session.query(Answer).filter(Answer.id == instance.id).one_or_none()

        if answer:
            answer.content = instance.content

            if not answer.author_url and instance.author_url:
                answer.author_url = instance.author_url
                answer.author = instance.author
                answer.author_name = instance.author_name

            answer.collect_num = instance.collect_num
            answer.comment_num = instance.comment_num
            answer.upvote_num = instance.upvote_num

            answer.deleted = instance.deleted
            updated(answer, update)
        else:
            updated(instance, update)
            session.add(instance)


def updated(instance, update):
    if update == TYPES[0]:
        instance.hot_updated_at = text('NOW()')
    if update == TYPES[1]:
        instance.top_updated_at = text('NOW()')
    instance.updated_at = text('NOW()')
