# -*- coding: utf-8 -*-
"""
Allows you to make some functions to run in parallel using @async_call decorator and wait_task() function.
https://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python
"""
from threading import Thread
from Queue import Queue


class ParallelTasks(object):
    def __init__(self):
        self.queue = None
        self.threads = []
        self.no_more_tasks = False

    def do_work(self):
        """ Does some work """
        while not self.no_more_tasks:
            func, args = self.queue.get()
            func(*args)
            self.queue.task_done()

    def wait_ending(self):
        """ Waits until all tasks are completed """
        if self.queue:
            self.queue.join()
            self.no_more_tasks = True

            @self.async_call
            def nothing(): pass
            [ nothing() for _ in self.threads ]
            self.queue.join()
            self.queue = None
            [ thread.join() for thread in self.threads ]

    def __start_work(self, threads=10):
        if not self.queue:
            self.queue = Queue()
            self.threads = []
            self.no_more_tasks = False
            for i in range(threads):
                thread = Thread(target=self.do_work)
                thread.daemon = True
                thread.start()
                self.threads.append(thread)

    def async_call(self, func):
        """ Decorator that sends a task in background when the funcion with it is called """
        self.__start_work()

        def call(*args):
            self.queue.put((func, args))
        return call
