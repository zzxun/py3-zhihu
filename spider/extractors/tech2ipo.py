#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/28

""" Description: download tech2ipo and parser all
"""

from spider.database import News, auto_session
from spider.config import TECH2IPO_URL
from spider.common import wait


def process(url_generator, session, tag='', sleep=5):
    """: all json data, just get and store it
    :param url_generator: urls
    :param session: requests
    :param tag: tag of url
    :param sleep: sleep for safe
    """
    for url in url_generator:

        print('Process news ' + url)

        try:

            # get
            res = session.get(url)

            wait(sleep)

            # parser
            json_data = res.json()
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

                    auto_session(News.create, News(source='tech2ipo',
                                                   tag=tag,
                                                   url=url,
                                                   title=title,
                                                   image=image,
                                                   summary=summary))

            else:
                return

        except Exception as e:
            print(e)
            # return now for duplicate
            return
