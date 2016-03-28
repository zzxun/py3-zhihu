#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description: news main thread
"""

import requests


def get_news(args):
    """:get all news's title url img_url summary,
        tech2ipo/pingwest/sspai/tech163
    :param args: args.concurrency int
    """

    from .pool import ThreadPool
    from multiprocessing import cpu_count
    from .config import NEWS_URLS
    from .common import Default_Header

    concurrency = args.concurrency or cpu_count() * 2

    thread_pool = ThreadPool(concurrency)

    for (key, tags) in NEWS_URLS.items():
        exec('from .extractors.%s import process' % (key,))
        exec('from .config import %s' % (key,))
        session = requests.session()
        session.headers.update(Default_Header)
        for tag in tags:
            exec('thread_pool.submit(process, %s("%s"), session, "%s")'
                 % (key, tag, tag))

    thread_pool.wait_completion()
