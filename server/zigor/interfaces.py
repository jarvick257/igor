from typing import Callable, Any, Optional

from .content import Content
from .encoder import EncoderAction
from .display_update import DisplayUpdate


class IDisplay:
    def on_input(self, action: EncoderAction) -> None:
        _ = action
        raise NotImplementedError()

    def render(self) -> Content:
        raise NotImplementedError()

    def register(
        self,
        state: Any,
        callback: Callable[["IDisplay", DisplayUpdate, Optional["IDisplay"]], None],
    ) -> None:
        _ = callback, state
        raise NotImplementedError()

    def unregister(self):
        raise NotImplementedError()
