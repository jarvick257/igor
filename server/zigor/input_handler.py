from typing import Callable

from .encoder import EncoderAction


class InputHandler:
    def on_input(self, callback: Callable[[EncoderAction], None]) -> None:
        _ = callback
        raise NotImplementedError()

    def run(self) -> None:
        raise NotImplementedError()
