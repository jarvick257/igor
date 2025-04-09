from dataclasses import dataclass
from threading import Thread, Event
import zigor


@dataclass
class AppState:
    counter: int = 0


class HomeDisplay(zigor.Display):
    def get_content(self, state: AppState) -> zigor.Content:
        return zigor.Content("Home", f"counter: {state.counter}")

    def on_enter(self, state: AppState):
        self.push(CounterDisplay(state.counter))


class CounterDisplay(zigor.Display):
    def __init__(self, counter: int):
        self.counter = counter
        self.stopped = Event()
        self.timer = Thread(target=self.timeout)
        self.timer.start()

    def timeout(self):
        while not self.stopped.wait(1.0):
            self.counter += 1
            self.refresh()

    def get_content(self, state: AppState) -> zigor.Content:
        return zigor.Content("Set Counter", f"{state.counter} -> {self.counter}")

    def on_enter(self, state: AppState):
        self.stopped.set()
        self.timer.join()
        state.counter = self.counter
        self.pop()

    def on_next(self, state: AppState):
        self.counter += 1
        self.refresh()

    def on_prev(self, state: AppState):
        self.counter -= 1
        self.refresh()


mqtt_client = zigor.MqttClient("192.168.1.2", 1883)
app = zigor.App(AppState(), mqtt_client, mqtt_client)
app.run(HomeDisplay())
