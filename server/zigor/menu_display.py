from typing import List, Any
from .display import Display
from .content import Content


class MenuDisplay(Display):
    def __init__(self, title: str, options: List[str]):
        self.title: str = title
        self._options: List[str] = options
        self._counter = 0

    @property
    def selection(self) -> str:
        return self._options[self._counter]

    def get_content(self, state: Any) -> Content:
        return Content(self.title, self._options[self._counter])

    def on_next(self, state: Any):
        self._counter = (self._counter + 1) % len(self._options)
        self.refresh()

    def on_prev(self, state: Any):
        self._counter = (self._counter - 1) % len(self._options)
        self.refresh()
