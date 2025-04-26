from typing import Callable, Any, Optional

from .content import Content
from .encoder import EncoderAction
from .display_update import DisplayUpdate


class Display:
    def on_input(self, action: EncoderAction) -> None:
        _ = action
        raise NotImplementedError()

    def render(self) -> Content:
        raise NotImplementedError()

    def attach(
        self,
        state: Any,
        callback: Callable[["Display", DisplayUpdate, Optional["Display"]], None],
    ) -> None:
        _ = callback, state
        raise NotImplementedError()

    def detach(self):
        raise NotImplementedError()
