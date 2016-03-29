#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description: news main thread
"""

from asyncio import get_event_loop, ensure_future, wait
from .common import get_aio_session


def get_news(args):
    """:get all news's title url img_url summary,
        tech2ipo/pingwest/sspai/tech163
    :param args: args.concurrency int
    """

    from .config import NEWS_URLS

    loop = get_event_loop()

    tasks = []
    for (key, tags) in NEWS_URLS.items():
        tasks += _task(key, tags, loop)

    loop.run_until_complete(wait(tasks))


def _task(key, tags, loop):
    exec('from .extractors.%s import process' % (key,))
    exec('from .config import %s' % (key,))
    local = locals()
    return [ensure_future(
        local['process'](local[key](tag),
                         get_aio_session(loop), tag))
            for tag in tags]
