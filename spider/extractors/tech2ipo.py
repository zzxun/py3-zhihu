#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description: download tech2ipo and parser all
"""

from spider.database import News, Session
from spider.config import TECH2IPO_URL
from spider.common import wait, auto_close


@auto_close
async def process(url_generator, session, tag='', sleep=5):
    """: all json data, just get and store it
    :param url_generator: urls
    :param session: aiohttp.session
    :param tag: tag of url
    :param sleep: sleep for safe
    """

    for url in url_generator:

        print('Process news ' + url)

        # get
        async with session.get(url) as res:

            # parser
            json_data = await res.json()
            if json_data and json_data['data']['list']:
                # time desc
                results = json_data['data']['list']
                for r in results:
                    title = r['title']
                    url = TECH2IPO_URL + str(r['article_id'])
                    image = r['image'] or ''
                    if image:
                        image = image.replace('//', '/').replace('\n', '')
                    summary = r['summary'].strip()

                    News.create(Session(),
                                News(source='tech2ipo',
                                     tag=tag,
                                     url=url,
                                     title=title,
                                     image=image,
                                     summary=summary))

            else:
                return

        # for safe
        wait(sleep)
