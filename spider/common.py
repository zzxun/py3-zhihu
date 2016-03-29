#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/22

""" Description: utils functions
"""

import base64
from time import sleep as waitting
from random import uniform
from bs4 import BeautifulSoup as _Bs
from aiohttp import ClientSession


def auto_close(func):
    """
    :param func: wrap func
    :return: wrap func to close aiohttp session
    """

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            args[1].close()

    return wrapper


def beautiful_soup(makeup): return _Bs(makeup, 'lxml')


def encode_passwd(password: str):
    """ convert password
    :param password: origin or base64-password
    :return: base64-password
    """
    if password.startswith('$BASE64:'):
        return password
    return '$BASE64:' + base64.b64encode(password.encode()).decode()


def decode_passwd(password: str):
    """ convert password
    :param password: origin or base64-password
    :return: origin
    """
    if password.startswith('$BASE64:'):
        password = password[8:]
        # origin
        return base64.b64decode(password.encode()).decode()
    return password


Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0'}


def get_aio_session(loop=None, headers=Default_Header):
    return ClientSession(headers=headers, loop=loop)


def wait(seconds):
    waitting(uniform(0, seconds))
