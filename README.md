# Project RIGOR - The 'Remote' IGOR
This is the next evolution of the .

**Project RIGOR** is an evolution of the original [**Project IGOR**](https://github.com/UrbanCircles/igor) by UrbanCircles, with a focus on remote control and server-client architecture. The **R** in *RIGOR* stands for **Remote**, marking a shift from the on-chip processing of the original project to a more flexible and scalable system.

---

## Evolution from Igor

- **Original Igor**: Processed everything on the chip, with WiFi capabilities never utilized for remote interaction.
- **Project RIGOR**: Introduces a **server-client architecture** to decouple logic from the device.  
  - The **server** (written in Python) handles all complex logic and decision-making.
  - The **device** receives display instructions from the server and sends user inputs back to it.
  - This separation enables **easier updates**, **scalability**, and **integration with the full Python ecosystem**.
  - The server was written with a **strong focus on modularity** which makes it easy to pick and choose what functionality you want in **your** Project RIGOR

---

## Installation

Install via pip:

```bash
pip install project-rigor
```

## Getting Started

Here is an example of how you can create and combine different screens and modules to build your very own Project RIGOR.

Note that we're using the pomodoro module which you need to install with `pip install project-rigor-pomodoro`.
If you want to create your own modules, I recommend checking it out here [Pomodoro](https://github.com/jarvick257/rigor-pomodoro).

```python
from dataclasses import dataclass

from rigor import Content, Module, App, MqttClient
from rigor.screens import MenuScreen, TimedScreen

from pomodoro import Pomodoro()

class Submenu(MenuScreen):
    def __init__(self):
        super().__init__("Submenu", ["Save", "Option2", "Option3", "Go Back"])

    def on_enter(self):
        if self.selection == "Save":
            # TimedScreen will be shown for the specified time and then pop itself automatically
            # replace will pop the current screen before pushing a new screen.
            # So this is basically 'Save and Exit' with a success message
            self.replace(TimedScreen(1, "Success", "Saved"))

        if self.selection == "Go Back":
            # pop the current screen to go back
            self.pop()



@dataclass
class MyAppState:
    # Pomodoro is a RIGOR module
    pomodoro = Pomodoro()


class MyProjectRigor(MenuScreen[AppState]):
    def __init__(self):
        super().__init__("Home", ["Submenu", "Pomodoro"])

    def on_enter(self):
        if self.selection == "Submenu":
            self.push(Submenu())
        elif self.selection == "Pomodoro":
            self.push(self.state.pomodoro)


mqtt_client = MqttClient("192.168.1.2", 1883)
app = App(mqtt_client, mqtt_client)
app.run(MyAppState(), MyProjectRigor())
```

## Docker example

TODO


## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details. 
