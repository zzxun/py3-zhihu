#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description: parse sspai
"""
from spider.database import News, auto_session
from spider.common import wait, beautiful_soup


def process(url_generator, session, tag='', sleep=5):
    """: all json data, just get and store it
    :param url_generator: urls
    :param session: requests
    :param tag: tag
    :param sleep: sleep for safe
    """
    for url in url_generator:

        print('Process news ' + url)

        try:
            # get
            res = session.get(url)

            wait(sleep)

            # parser
            soup = beautiful_soup(res.content)

            titles = soup.find_all('h2', class_='title')

            if titles:

                images = soup.find_all('img', class_='lazy')
                summary = soup.find_all('div', class_='desc')

                for t, i, s in zip(titles, images, summary):
                    url = t.a['href']
                    title = i['alt']
                    image = i['data-src']
                    summary = s.text.strip()

                    auto_session(News.create, News(source='sspai',
                                                   tag=tag,
                                                   url=url,
                                                   title=title,
                                                   image=image,
                                                   summary=summary))
            else:
                return
        except Exception as e:
            print(e)
            return
