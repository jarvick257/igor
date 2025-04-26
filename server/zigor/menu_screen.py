from typing import List, Any, TypeVar
from .screen import Screen
from .content import Content

T = TypeVar("T")


class MenuScreen(Screen[T]):
    def __init__(self, title: str, options: List[str]):
        super().__init__()
        self.title: str = title
        self._options: List[str] = options
        self._counter = 0

    @property
    def selection(self) -> str:
        return self._options[self._counter]

    def render(self) -> Content:
        return Content(self.title, self._options[self._counter])

    def on_next(self):
        self._counter = (self._counter + 1) % len(self._options)
        self.refresh()

    def on_prev(self):
        self._counter = (self._counter - 1) % len(self._options)
        self.refresh()
