from dataclasses import dataclass

from rigor import Content, Module, App, MqttClient
from rigor.screens import MenuScreen, AutoRefreshScreen, TimedScreen

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

    def render(self) -> Content:
        return Content("Set Counter", f"{self.state.count} -> {self.counter}")

    def on_enter(self):
        self.state.count = self.counter
        self.pop()

    def on_next(self):
        self.counter += 1
        self.refresh()

    def on_prev(self):
        self.counter -= 1
        self.refresh()


class CounterModule(Module[CounterState]):
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

    def render(self) -> Content:
        text: str = self.selection
        if self.selection == "Counter":
            text = f"Counter: {self.counter.count}"
        return Content(self.title, text)

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
        super().__init__("Submenu", ["Save", "Option2", "Option3", "Go Back"])

    def on_enter(self):
        if self.selection == "Save":
            self.replace(TimedScreen(1, "Success", "Saved"))

        if self.selection == "Go Back":
            self.pop()


mqtt_client = MqttClient("192.168.1.2", 1883)
app = App(mqtt_client, mqtt_client)
app.run(AppState(), HomeDisplay())
