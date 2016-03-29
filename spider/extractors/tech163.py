#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description: parse sspai
"""
from spider.database import News, Session
from spider.common import wait, beautiful_soup, auto_close


@auto_close
async def process(url_generator, session, tag='', sleep=5):
    """: all json data, just get and store it
    :param url_generator: urls
    :param session: requests
    :param tag: tag
    :param sleep: sleep for safe
    """

    for url in url_generator:

        print('Process news ' + url)

        # get
        async with session.get(url) as res:

            content = await res.text()
            # parser
            soup = beautiful_soup(content)

            titles = soup.find_all('h3', class_='bigsize')
            images = soup.find_all('a', class_='newsList-img')
            summary = soup.find_all('div', class_='newsDigest')

            for t, i, s in zip(titles, images, summary):
                url = t.a['href']
                title = t.text
                image = i.img['src']
                summary = s.text.strip()

                News.create(Session(),
                            News(source='tech163',
                                 tag=tag,
                                 url=url,
                                 title=title,
                                 image=image,
                                 summary=summary))

        wait(sleep)
