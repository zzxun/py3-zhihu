#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/19

""" Description:
"""

from spider.database import *
from spider.common import wait


def get_topic(client, url, thread_pool, limit, types=None, sleep=3):
    """:get topic content
    :param client: zhihu.ZhihuClient
    :param url: topc url
    :param thread_pool: handler function
    :param limit: limit question numbers
    :param types: hot / top / all
    :param sleep: sleep(seconds) for safe
    :return: generator topic.hot_questions, generator topic.top_answers
    """

    from pybloom import BloomFilter

    bloom = BloomFilter(capacity=50000, error_rate=0.001)

    # begin
    topic = client.topic(url)

    do_topic(topic)

    # three generator
    if 'hot' in types:
        thread_pool.submit(get_answers,
                           topic.hot_answers, thread_pool, limit, sleep, 'hot')
    if 'top' in types:
        thread_pool.submit(get_answers,
                           topic.top_answers, thread_pool, limit, sleep, 'top')
    if 'all' in types:
        thread_pool.submit(get_questions,
                           topic.questions, topic.id, thread_pool, limit, sleep, bloom)

    if 'tips' in types:
        for t in topic.children:
            do_topic(t, (t.id, topic.id))
        for t in topic.parents:
            do_topic(t, (topic.id, t.id))


def do_topic(topic, associate=None):
    try:
        # update or create
        db_topic = Topic(id=topic.id, tid=topic.tid,
                         url=topic.url, name=topic.name,
                         photo_url=topic.photo_url,
                         description=topic.description,
                         follower_num=topic.follower_num)

        print('Process topic %s' % topic.url)

        auto_session_except(Topic.create_or_update, db_topic)

        if associate:
            auto_session_except(TopicAssociate.create, *associate)
            print('Link topic %d to topic %d' % associate)

    except Exception as e:
        print(e)


def get_answers(answers, thread_pool, limit=1, sleep=3, update=None):
    """: top/hot answers
    :param answers: generator
    :param thread_pool: pool to submit
    :param limit: number questions limit
    :param sleep: sleep(seconds) for safe
    :param update: for answer top_updated_at or hot_updated_at or none
    :return:
    """
    last, count = None, 0
    for answer in answers:
        # for safe
        wait(sleep)
        if count > limit:
            return
        if answer.question.id != last:
            last = answer.question.id
            count += 1

        thread_pool.submit(get_answer,
                           answer, update)


def get_answer(answer, update=None):
    try:
        print('Process answer %s' % answer.url)
        db_answer = Answer(id=answer.id, aid=answer.aid,
                           url=answer.url, content=answer.content,
                           question=answer.question.id,
                           author_url=answer.author.url,
                           author=answer.author.id,
                           author_name=answer.author.name,
                           collect_num=answer.collect_num,
                           comment_num=answer.comment_num,
                           upvote_num=answer.upvote_num,
                           deleted=answer.deleted)
        auto_session_except(Answer.create_or_update, db_answer, update)

    except Exception as e:
        print(e)


def get_questions(questions, topic_id, thread_pool, limit, sleep, bloom):
    """
    :param questions: zhihu.Question
    :param topic_id: question associate to topic
    :param thread_pool
    :param limit: number questions limit
    :param sleep: sleep(seconds) for safe
    :return:
    """
    for question in questions:
        wait(sleep)

        try:
            auto_session_except(QuestionTopic.create, question.id, topic_id)
            print('Link question %d to topic %d' % (question.id, topic_id))
        except Exception as e:
            print(e)

        if bloom.add(question.url):
            continue

        if limit <= 0:
            return
        thread_pool.submit(get_question,
                           question, topic_id, thread_pool, sleep)
        limit -= 1


def get_question(question, topic_id, thread_pool, sleep=3):
    """:parser each question
    :param question: zhihu.Question
    :param topic_id: question associate to topic
    :param thread_pool
    :param sleep: sleep(seconds) for safe
    """
    try:
        wait(sleep)

        print('Process question %s' % question.url)

        db_question = Question(id=question.id, qid=question.qid,
                               url=question.url, title=question.title,
                               description=question.details,
                               author=question.author.url and question.author.id,
                               author_url=question.author.url,
                               deleted=question.deleted, follower_num=question.follower_num,
                               answer_num=question.answer_num,
                               creation_time=question.creation_time,
                               last_edit_time=question.last_edit_time)
        auto_session_except(Question.create_or_update, db_question)

        if question.answer_num > 0:
            thread_pool.submit(get_answers,
                               question.answers, thread_pool, 1, sleep, None)
    except Exception as e:
        print(e)
