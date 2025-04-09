from typing import NoReturn
from dataclasses import dataclass

from .display_update import DisplayUpdate

from .encoder import EncoderAction
from .display_stack import DisplayStack
from .display import Display

from .input_handler import InputHandler
from .output_handler import OutputHandler


class App:
    def __init__(
        self, state, input_handler: InputHandler, output_handler: OutputHandler
    ):
        self.state = state
        self.stack = DisplayStack()
        self.output_handler = output_handler
        self.input_handler = input_handler
        self.input_handler.on_input(self._on_input)

    def _on_input(self, action: EncoderAction) -> None:
        self.stack.peek().on_input(action, self.state)

    def _on_update(self, op: DisplayUpdate, display: Display | None) -> None:
        if op == DisplayUpdate.NONE:
            return
        elif op == DisplayUpdate.UPDATE:
            pass
        elif op == DisplayUpdate.PUSH:
            assert display != None
            self._add_display(display)
        elif op == DisplayUpdate.POP:
            self.stack.pop()
        self._render()

    def _render(self):
        self.output_handler.render(self.stack.peek().get_content(self.state))

    def _add_display(self, display: Display) -> None:
        display.update_callback = self._on_update
        self.stack.push(display)

    def run(self, display: Display) -> None:
        self._add_display(display)
        self._render()
        self.input_handler.run()
