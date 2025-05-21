from typing import Callable

from rigor import Content
from rigor.screens import Screen


class InputNumberScreen(Screen[None]):
    def __init__(self, title: str, minutes: int, on_enter: Callable[[int], None]):
        self.title: str = title
        self.minutes: int = minutes
        self.on_enter_callback: Callable[[int], None] = on_enter

    def render(self) -> Content:
        return Content(self.title, str(self.minutes))

    def on_enter(self):
        self.on_enter_callback(self.minutes)
        self.pop()

    def on_prev(self):
        self.minutes = max(self.minutes - 1, 0)
        self.refresh()

    def on_next(self):
        self.minutes += 1
        self.refresh()
