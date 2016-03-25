#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/22

""" Description: utils functions
"""

import base64


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
