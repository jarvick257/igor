from dataclasses import dataclass

import zigor


@dataclass
class PomodoroState:
    foo = "bar"


class PomodoroMain(zigor.Display[PomodoroState]):
    def render(self) -> zigor.Content:
        return zigor.Content("Pomodoro", f"Hello from {self.state.foo}")

    def on_enter(self):
        self.pop()

    def on_next(self):
        self.refresh()


class Pomodoro(zigor.Module[PomodoroState]):
    def __init__(self):
        super().__init__(PomodoroState(), PomodoroMain())

    def preview(self) -> zigor.Content:
        return zigor.Content("Pomodoro", "Focus like a tomato")
