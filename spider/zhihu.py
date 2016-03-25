#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/22

""" Description:
"""
from multiprocessing import cpu_count
from zhihu import ZhihuClient
from .database import *
from .utils import *
from .cli import ARGS_PRRSER

CLIENTS = []


def get_topic(args):
    """ :get topic 动态(hot) / 精华(top)
    :param args: args.url list(str),
                 args.type list(str),
                 args.limit int,
                 args.concurrency int,
                 args.sleep int
    """

    if not args.url:
        ARGS_PRRSER.print_help()
        return

    from .pool import ThreadPool
    from .extractors.topic import DEFAULT_TYPES, TYPES, get_topic
    from sys import maxsize

    urls = set(args.url)
    types = args.type or DEFAULT_TYPES
    limit = args.limit if args.limit and args.limit > 0 else maxsize
    concurrency = args.concurrency or cpu_count()
    sleep_seconds = args.sleep or 3

    # initial types
    tmp = []
    for t in TYPES:
        if t in types:
            tmp.append(t)
    types = TYPES if len(tmp) == 0 else tmp

    # thread pool
    thread_pool = ThreadPool(concurrency)

    # get topic
    for url in urls:
        thread_pool.submit(get_topic,
                           get_client(),
                           url,
                           thread_pool,
                           limit,
                           types,
                           sleep_seconds)

    thread_pool.wait_completion()


def add_or_update(args):
    """
    :param args: username list and password list
    """
    usernames = args.username
    passwords = args.password

    if len(usernames) != len(passwords):
        raise TypeError('username and password not in pairs')

    for i in range(len(usernames)):

        client = ZhihuClient()
        password = decode_passwd(passwords[i])

        code, msg, cookies = client.login(usernames[i], password, '')

        if code == 0:
            print('login successfully')
            auto_session(Cookie.add_or_update, usernames[i], password, cookies)
        else:
            print('login failed, reason: {0}'.format(msg))
            auto_session(Cookie.clean_cookies, usernames[i])


def list_cookies_and_print(args):
    cs = auto_session(Cookie.get_all_cookies)
    print(cs)


def get_client():
    for cookie in auto_session(Cookie.get_all_cookies):
        CLIENTS.append(ZhihuClient(cookie.cookie))
    if not CLIENTS:
        raise Exception('None cookies found')
    return CLIENTS[0]
