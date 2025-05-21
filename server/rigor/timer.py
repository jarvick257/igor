from typing import Callable
from threading import Thread, Event


class Timer:
    def __init__(self, interval_seconds: float, callback: Callable):
        self._interval_seconds: float = interval_seconds
        self._stopped = Event()
        self._timer: Thread | None = None
        self._callback = callback

    def start(self):
        self._stopped = Event()
        self._timer = Thread(target=self._timeout)
        self._timer.start()

    def stop(self):
        self._stopped.set()
        if self._timer is not None:
            self._timer.join()

    def _timeout(self):
        while not self._stopped.wait(self._interval_seconds):
            self._callback()
