#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/14

""":Description: Main Entry
"""

import logging
from spider import *

logging.BASIC_FORMAT = '%%(levelname)s - %(filename)s[%(lineno)d]- %(message)s'
logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
requests_log = logging.getLogger('requests.packages.urllib3')
requests_log.setLevel(logging.ERROR)
requests_log.propagate = True

subparsers = ARGS_PRRSER.add_subparsers(dest='command', help='commands')

# `user` command
# user -u xtkml.g@gmail.com -p $BASE64:eHVuc2hvbWU=
group_user = subparsers.add_parser('user',
                                   description='Zhihu users, not exist => add new, exist=>update password/cookies')
group_user.add_argument('-u', '--username', type=str, metavar='u', nargs='+')
group_user.add_argument('-p', '--password', type=str, metavar='p', nargs='+')
group_user.set_defaults(func=add_or_update)

# `topic` command
# topic -u https://www.zhihu.com/topic/19805484
group_topic = subparsers.add_parser('topic', description='Example: -u https://www.zhihu.com/topic/19805484')
group_topic.add_argument('-u', '--url', type=str, metavar='url', nargs='+',
                         help='list zhihu topic urls')
group_topic.add_argument('-t', '--type', type=str, metavar='t', nargs='*',
                         help='hot/top: hot_questions/top_answers, default hot top')
group_topic.add_argument('-l', '--limit', type=int, metavar='l', nargs='?',
                         help='question number limit, default parser head 20')
group_topic.add_argument('-c', '--concurrency', type=int, metavar='cc', nargs='?',
                         help='concurrency Process, default CPUs')
group_topic.add_argument('-s', '--sleep', type=int, metavar='s', nargs='?',
                         help='sleep (seconds) after each http request, default 3s')
group_topic.set_defaults(func=get_topic)

# `cookie` command
group_cookie = subparsers.add_parser('cookie',
                                     description='Show zhihu users cookies')
group_cookie.set_defaults(func=list_cookies_and_print)

if __name__ == '__main__':
    # args = ARGS_PRRSER.parse_args('topic -u https://www.zhihu.com/topic/19805484 -t tips -s 3 -l 1'.split())
    # args = ARGS_PRRSER.parse_args('topic -h'.split())
    args = ARGS_PRRSER.parse_args()
    args.func(args)
