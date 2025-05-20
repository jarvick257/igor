from dataclasses import dataclass

import zigor
from zigor.screens import MenuScreen, AutoRefreshScreen

from pomodoro import Pomodoro


@dataclass
class CounterState:
    count: int = 0


class CounterEditDisplay(AutoRefreshScreen[CounterState]):
    def __init__(self):
        super().__init__(1.0)
        self.counter = 0

    def on_attach(self):
        self.counter = self.state.count
        super().on_attach()

    def on_timeout(self):
        self.counter += 1

    def render(self) -> zigor.Content:
        return zigor.Content("Set Counter", f"{self.state.count} -> {self.counter}")

    def on_enter(self):
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


class HomeDisplay(MenuScreen[AppState]):
    def __init__(self):
        super().__init__("Home", ["Submenu", "Counter", "Pomodoro"])

    @property
    def counter(self):
        return self.state.counter.state

    @property
    def pomodoro(self):
        return self.state.pomodoro.state

    def render(self) -> zigor.Content:
        text: str = self.selection
        if self.selection == "Counter":
            text = f"Counter: {self.counter.count}"
        return zigor.Content(self.title, text)

    def on_enter(self):
        match self.selection:
            case "Counter":
                self.push(self.state.counter)
            case "Pomodoro":
                self.push(self.state.pomodoro)
            case "Submenu":
                self.push(SubmenuDisplay())


class SubmenuDisplay(MenuScreen):
    def __init__(self):
        super().__init__("Submenu", ["Option1", "Option2", "Option3", "Go Back"])

    def on_enter(self):
        if self.selection == "Go Back":
            self.pop()


mqtt_client = zigor.MqttClient("192.168.1.2", 1883)
app = zigor.App(mqtt_client, mqtt_client)
app.run(AppState(), HomeDisplay())
