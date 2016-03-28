#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description:
"""

from urllib import parse

"""
:use locals()['sspai']('智能硬件')
"""
NEWS_URLS = {
    'tech2ipo': ['物联网', '无人机', '虚拟现实', '智能硬件', '人工智能'],
    'pingwest': ['智能硬件', '虚拟现实', '智能家居', '无人机', '人工智能', '机器人'],
    'sspai': ['硬件'],
    'tech163': ['']
}

TECH2IPO_URL = 'http://tech2ipo.com/'


def tech2ipo(tag):
    """: return a generator of getting next url
    :param tag: above tags
    :return: generator
    """
    from time import time
    url = TECH2IPO_URL + 'tag/%s/list?_=%d' % (parse.quote(tag), int(time() * 1000))
    index = 0
    while True:
        yield url + '&index=' + str(index)
        index += 1


def pingwest(tag):
    url = 'http://www.pingwest.com/tag/%s/' % (parse.quote(tag),)
    index = 1
    while True:
        yield url + 'page/' + str(index) + '/'
        index += 1


def sspai(tag):
    url = 'http://sspai.com/tag/%s/' % (parse.quote(tag),)
    index = 1
    while True:
        yield url + '?page=' + str(index)
        index += 1


def tech163(tag=''):
    """: no more for 163 tech
    :param tag: default ''
    :return: generator whith one
    """
    yield 'http://tech.163.com/special/intelligent-hot/'
