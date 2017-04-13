# encoding: utf-8

import threading

__author__ = 'BetaS'


class Thread:
    def __init__(self):
        self._running = False
        self._thread = threading.Thread(target=self._run)

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()

    def _run(self):
        self.onStart()

        self.onUpdate()

        while self._running:
            self.onUpdate()

        self.onStop()

    def onStart(self):
        pass

    def onStop(self):
        pass

    def onUpdate(self):
        pass


class Coroutine(Thread):
    def start(self):
        self._thread.start()