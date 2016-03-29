#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description: http://www.pingwest.com/tag/
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

                News.create(Session(),
                            News(source='pingwest',
                                 tag=tag,
                                 url=url,
                                 title=title,
                                 image=image,
                                 summary=summary))

        wait(sleep)
