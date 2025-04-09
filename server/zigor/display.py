from loguru import logger
from typing import Any, Optional, Callable
from .encoder import EncoderAction
from .content import Content
from .display_update import DisplayUpdate


class Display:
    def __init__(self):
        self.enabled: bool = False
        self.update_callback: Callable[[DisplayUpdate, Display | None], None] | None = (
            None
        )

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def on_input(self, action: EncoderAction, state: Any) -> None:
        if action == EncoderAction.NONE:
            self.on_nop(state)
        elif action == EncoderAction.ENTER:
            self.on_enter(state)
        elif action == EncoderAction.NEXT:
            self.on_next(state)
        elif action == EncoderAction.PREV:
            self.on_prev(state)

    def on_nop(self, state: Any) -> None:
        _ = state

    def on_enter(self, state: Any) -> None:
        _ = state

    def on_next(self, state: Any) -> None:
        _ = state

    def on_prev(self, state: Any) -> None:
        _ = state

    def get_content(self, state: Any) -> Content:
        _ = state
        raise NotImplementedError()

    def _update(self, op: DisplayUpdate, display: Optional["Display"] = None):
        if not self.enabled or self.update_callback is None:
            logger.warning(
                f"Ignoring {op}. enabled: {self.enabled=} - callback: {self.update_callback is not None}"
            )
            return
        self.update_callback(op, display)

    def skip(self):
        self._update(DisplayUpdate.NONE)

    def pop(self):
        self._update(DisplayUpdate.POP)

    def push(self, display: "Display"):
        self._update(DisplayUpdate.PUSH, display)

    def refresh(self):
        self._update(DisplayUpdate.UPDATE)
