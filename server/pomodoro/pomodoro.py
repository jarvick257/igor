from enum import Enum
from datetime import datetime, timedelta
from typing import List
from dataclasses import dataclass

from zigor import Content, Module, Timer
from zigor.screens import (
    InputNumberScreen,
    MenuScreen,
    TimedScreen,
)


class PomodoroTask(Enum):
    Task = 1
    ShortBreak = 2
    LongBreak = 3


@dataclass
class PomodoroState:
    pomodori_count: int = 0
    minutes_per_task: int = 25
    minutes_per_short_break: int = 5
    minutes_per_long_break: int = 20
    tasks_before_long_break: int = 4
    timer_start: datetime | None = None

    def reset(self):
        self.timer_start = None
        self.pomodori_count = 0

    def task_sequence(self) -> List[PomodoroTask]:
        l = []
        for _ in range(self.tasks_before_long_break - 1):
            l += [PomodoroTask.Task, PomodoroTask.ShortBreak]
        l += [PomodoroTask.Task, PomodoroTask.LongBreak]
        return l


class PomodoroTaskScreen(MenuScreen[PomodoroState]):
    def __init__(self):
        super().__init__("Task", ["Remaining", "Clock", "Task"])
        self._timer = Timer(1, self.on_timeout)

    def on_attach(self):
        self._timer.start()

    def on_detach(self):
        self._timer.stop()

    def _current_task(self) -> PomodoroTask:
        tasks = self.state.task_sequence()
        index = self.state.pomodori_count % len(tasks)
        return tasks[index]

    def _task_duration(self) -> timedelta:
        current_task = self._current_task()
        if current_task == PomodoroTask.ShortBreak:
            return timedelta(minutes=self.state.minutes_per_short_break)
        if current_task == PomodoroTask.LongBreak:
            return timedelta(minutes=self.state.minutes_per_long_break)
        return timedelta(minutes=self.state.minutes_per_task)

    def _elapsed(self) -> timedelta:
        if self.state.timer_start is None:
            self.state.timer_start = datetime.now()
        return datetime.now() - self.state.timer_start

    def on_timeout(self):
        duration = self._task_duration()
        elapsed = self._elapsed()
        if elapsed < duration:
            self.refresh()
            return
        self.state.pomodori_count += 1
        self.state.timer_start = datetime.now()
        new_task = self._current_task()
        if new_task == PomodoroTask.Task:
            self.push(TimedScreen(5, "Break's over", "Back to work!"))
        elif new_task == PomodoroTask.ShortBreak:
            self.push(TimedScreen(5, "Done", "Short Break"))
        elif new_task == PomodoroTask.LongBreak:
            self.push(TimedScreen(5, "Done", "Long Break"))

    def _render_remaining(self) -> Content:
        task = self._current_task()
        duration = self._task_duration()
        elapsed = self._elapsed()
        minutes, seconds = divmod(round((duration - elapsed).total_seconds()), 60)
        body = f"{minutes:02d}:{seconds:02d}"
        if elapsed.total_seconds() > 10:
            title = "Remaining"
        elif task == PomodoroTask.ShortBreak:
            title = "Short Break"
        elif task == PomodoroTask.LongBreak:
            title = "Long Break"
        else:
            title = "Work"
        return Content(title, body)

    def render(self) -> Content:
        if self.selection == "Clock":
            return Content("Clock", datetime.now().strftime("%H:%M"))
        if self.selection == "Task":
            task = self._current_task()
            body = task.name
            if task == PomodoroTask.Task:
                body = f"Task {self.state.pomodori_count // 2 + 1}"
            return Content("Task", body)

        return self._render_remaining()

    def on_enter(self):
        self.pop()


class PomodoroSettingsScreen(MenuScreen[PomodoroState]):
    def __init__(self):
        super().__init__("Settings", ["Task", "Short Break", "Long Break", "Back"])

    def _set_task_length(self, n: int):
        self.state.minutes_per_task = n

    def _set_short_break_length(self, n: int):
        self.state.minutes_per_short_break = n

    def _set_long_break_length(self, n: int):
        self.state.minutes_per_long_break = n

    def on_enter(self):
        if self.selection == "Back":
            self.pop()
        elif self.selection == "Task":
            self.push(
                InputNumberScreen(
                    "Task Minutes",
                    self.state.minutes_per_task,
                    self._set_task_length,
                )
            )
        elif self.selection == "Short Break":
            self.push(
                InputNumberScreen(
                    "Short Break",
                    self.state.minutes_per_short_break,
                    self._set_short_break_length,
                )
            )
        elif self.selection == "Long Break":
            self.push(
                InputNumberScreen(
                    "Long Break",
                    self.state.minutes_per_long_break,
                    self._set_long_break_length,
                )
            )


class PomodoroResetScreen(MenuScreen[PomodoroState]):
    def __init__(self):
        super().__init__("Reset", ["Back", "Confirm"])

    def on_enter(self):
        if self.selection == "Back":
            self.pop()
        if self.selection == "Confirm":
            self.state.reset()
            self.replace(TimedScreen(2, "Success", "Tasks Cleared"))


class PomodoroMainScreen(MenuScreen[PomodoroState]):
    def __init__(self):
        super().__init__("Pomodoro", ["Task", "Reset", "Settings", "Back"])

    def on_enter(self):
        if self.selection == "Back":
            self.pop()
        elif self.selection == "Task":
            self.push(PomodoroTaskScreen())
        elif self.selection == "Settings":
            self.push(PomodoroSettingsScreen())
        elif self.selection == "Reset":
            self.push(PomodoroResetScreen())


class Pomodoro(Module[PomodoroState]):
    def __init__(self):
        super().__init__(PomodoroState(), PomodoroMainScreen())

    def preview(self) -> Content:
        return Content("Pomodoro", "Focus like a tomato")
