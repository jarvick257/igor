from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from threading import Thread, Event
import zigor

from pomodoro import Pomodoro


@dataclass
class CounterState:
    count: int = 0


class CounterEditDisplay(zigor.Display[CounterState]):
    def __init__(self):
        self.counter = 0
        self.stopped = Event()

    def on_registered(self):
        print("Registered Counter")
        self.counter = self.state.count
        self.stopped = Event()
        self.timer = Thread(target=self.timeout)
        self.timer.start()

    def on_unregistered(self):
        print("UNRegistered Counter")

    def timeout(self):
        while not self.stopped.wait(1.0):
            self.counter += 1
            self.refresh()

    def render(self) -> zigor.Content:
        return zigor.Content("Set Counter", f"{self.state.count} -> {self.counter}")

    def on_enter(self):
        self.stopped.set()
        self.timer.join()
        self.state.count = self.counter
        self.pop()

    def on_next(self):
        self.counter += 1
        self.refresh()

    def on_prev(self):
        self.counter -= 1
        self.refresh()


class CounterModule(zigor.Module[CounterState]):
    def __init__(self, initial_count: int = 0):
        super().__init__(CounterState(initial_count), CounterEditDisplay())


@dataclass
class AppState:
    counter = CounterModule()
    pomodoro = Pomodoro()


class HomeDisplay(zigor.MenuDisplay[AppState]):
    def __init__(self):
        super().__init__("Home", ["Submenu", "Counter", "Pomodoro"])

    def render(self) -> zigor.Content:
        text: str = self.selection
        if self.selection == "Counter":
            if self.state.counter is None:
                text = f"Counter: 0"
            else:
                text = f"Counter: {self.state.counter.state.count}"
        elif self.selection == "Pomodoro":
            return self.state.pomodoro.preview()
        return zigor.Content(self.title, text)

    def on_enter(self):
        print(self.state)
        match self.selection:
            case "Counter":
                self.push(self.state.counter)
            case "Pomodoro":
                self.push(self.state.pomodoro)
            case "Submenu":
                self.push(SubmenuDisplay())


class SubmenuDisplay(zigor.MenuDisplay):
    def __init__(self):
        super().__init__("Submenu", ["Option1", "Option2", "Option3", "Go Back"])

    def on_enter(self):
        if self.selection == "Go Back":
            self.pop()


mqtt_client = zigor.MqttClient("192.168.1.2", 1883)
app = zigor.App(mqtt_client, mqtt_client)
app.run(AppState(), HomeDisplay())
