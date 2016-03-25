#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/17

""" Description: a dic
"""

from sqlalchemy import Column, Integer, Sequence, UniqueConstraint
from .base import Base


class TopicAssociate(Base):
    __tablename__ = 'topic_associate'
    __table_args__ = (
        UniqueConstraint('topic', 'parent', name='IDX_TOPIC_PARENT'),
    )

    id = Column(Integer, Sequence('topic_associate_id_seq'), primary_key=True)
    # zhihu id
    topic = Column(Integer, nullable=False, index=True)
    # multi parents, multi childrens
    parent = Column(Integer, nullable=False, index=True)

    @classmethod
    def create(cls, session, topic_id, parent_id):
        session.add(TopicAssociate(topic=topic_id, parent=parent_id))
