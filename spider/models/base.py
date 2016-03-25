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
