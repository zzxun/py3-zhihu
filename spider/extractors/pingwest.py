#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description: http://www.pingwest.com/tag/
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

            titles = soup.find_all('h2')

            if '404' in titles[0].text:
                return

            titles = titles[1:]
            images = soup.find_all('div', class_='thumb-img')
            summary = soup.find_all('p', class_='des')

            for t, i, s in zip(titles, images, summary):
                url = t.a['href']
                title = t.a.text
                image = i.a.img['src']
                summary = s.text.strip()

                auto_session(News.create, News(source='pingwest',
                                               tag=tag,
                                               url=url,
                                               title=title,
                                               image=image,
                                               summary=summary))
        except Exception as e:
            print(e)
            return
