#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/17

""" Description: a dic
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql.expression import text, false
from .base import Base, updated
from datetime import datetime


class Question(Base):
    __tablename__ = 'question'

    # zhihu id
    id = Column(Integer, primary_key=True)
    qid = Column(Integer)

    url = Column(String(100), unique=True, nullable=False)

    title = Column(String(100), nullable=False)
    description = Column(Text)

    author_url = Column(String(100), nullable=False, server_default='')
    author = Column(String(100), nullable=False, server_default='')

    follower_num = Column(Integer, nullable=False, server_default=text('0'))
    answer_num = Column(Integer, nullable=False, server_default=text('0'))

    creation_time = Column(DateTime, nullable=False, server_default=text('NOW()'))
    last_edit_time = Column(DateTime, nullable=False, server_default=text('NOW()'))

    deleted = Column(Boolean, nullable=False, server_default=false())

    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))
    updated_at = Column(DateTime, nullable=False, server_default=text('NOW()'),
                        onupdate=datetime.now)

    @classmethod
    def create_or_update(cls, session, instance):
        question = session.query(Question).filter(Question.id == instance.id).one_or_none()

        if question:
            question.title = instance.title
            question.description = instance.description
            question.follower_num = instance.follower_num
            question.answer_num = instance.answer_num
            question.last_edit_time = instance.last_edit_time
            question.deleted = instance.deleted
            updated(question)
        else:
            session.add(instance)
