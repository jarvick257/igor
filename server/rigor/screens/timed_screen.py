from threading import Timer

from rigor import Content
from rigor.screens import Screen


class TimedScreen(Screen[None]):
    def __init__(self, seconds: float, title: str, body: str):
        self.title: str = title
        self.body: str = body
        self.timer = Timer(seconds, self.pop)
        self.timer.start()

    def render(self) -> Content:
        return Content(self.title, self.body)
