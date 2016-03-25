#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/17

""" Description: a dic
"""

from sqlalchemy import Column, Integer, Sequence, UniqueConstraint
from .base import Base


class QuestionTopic(Base):
    __tablename__ = 'question_topic'
    __table_args__ = (
        UniqueConstraint('topic', 'question', name='IDX_TOPIC_QUESTION'),
    )

    id = Column(Integer, Sequence('question_topic_id_seq'), primary_key=True)
    # zhihu id
    question = Column(Integer, nullable=False, index=True)
    topic = Column(Integer, nullable=False, index=True)

    @classmethod
    def create(cls, session, question_id, topic_id):
        session.add(QuestionTopic(question=question_id, topic=topic_id))
