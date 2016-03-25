#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author: zzxun <xtkml.g@gamil.com>
# date: 16/3/22

""" Description:
"""
from queue import Queue
from threading import Thread


class Worker(Thread):
    RUN_FLAG = True

    """:Thread executing tasks from a given tasks queue"""

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.setDaemon(True)
        self.run_flag = Worker.RUN_FLAG
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def submit(self, func, *args, **kargs):
        """ Add a task to the queue
        :param func: execute function
        :param args: args
        :param kargs: kargs
        """
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


def test():
    from random import randrange
    from time import sleep, time
    from concurrent.futures import ThreadPoolExecutor

    delays = [randrange(1, 10) for i in range(100)]

    def wait_delay(d):
        print('sleeping for (%d)sec' % d)
        sleep(d)

    start = time()

    pool = ThreadPool(20)

    # pool = ThreadPoolExecutor(20)

    for i, d in enumerate(delays):
        pool.submit(wait_delay, d)

        # pool.submit(wait_delay, d)
    pool.wait_completion()
    # pool.shutdown()

    end = time()

    print(end - start)
