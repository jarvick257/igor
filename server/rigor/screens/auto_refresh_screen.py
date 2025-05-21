from typing import TypeVar
from rigor.screens import Screen
from rigor import Timer

T = TypeVar("T")


class AutoRefreshScreen(Screen[T]):
    def __init__(self, interval_seconds: float):
        self._timer = Timer(interval_seconds, self._timeout)

    def on_attach(self):
        self._timer.start()

    def on_detach(self):
        self._timer.stop()

    def on_timeout(self):
        pass

    def _timeout(self):
        self.on_timeout()
        self.refresh()
