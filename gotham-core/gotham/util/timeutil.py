# encoding: utf-8

import time

__author__ = 'BetaS'


class AsyncTimer:
    def __init__(self, period=1.0):
        self._period = period
        self._last_run = 0

    def check(self):
        curr = time.time()
        if curr - self._last_run >= self._period:
            self._last_run = curr
            return True
        return False

    def last_run(self):
        return self._last_run

    def duration(self):
        curr = time.time()
        return curr - self._last_run

    def update(self):
        self._last_run = time.time()
