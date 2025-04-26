from typing import Callable, Any, Optional, TypeVar, Generic, List

from .content import Content
from .display_update import DisplayUpdate
from .encoder import EncoderAction

from .display import Display

T = TypeVar("T")


class Module(Generic[T], Display):
    def __init__(self, module_state: T, display: Display):
        self.state: T = module_state
        self.stack: List[Display] = []
        self._update_parent = None
        self._push(display)

    def _push(self, display: Display) -> None:
        self.stack.append(display)
        if self._update_parent is not None:
            display.attach(self.state, self._on_child_update)
            self._refresh()

    def _pop(self) -> None:
        if len(self.stack) > 1:
            self.stack[-1].detach()
            self.stack = self.stack[:-1]
            self._refresh()
        elif self._update_parent:
            self._update_parent(self, DisplayUpdate.POP, None)

    def _peek(self) -> Display:
        assert len(self.stack) > 0
        return self.stack[-1]

    def on_input(self, action: EncoderAction) -> None:
        self._peek().on_input(action)

    def render(self) -> Content:
        return self._peek().render()

    def attach(
        self,
        state: Any,
        callback: Callable[["Display", DisplayUpdate, Optional["Display"]], None],
    ) -> None:
        _ = state
        self._update_parent = callback
        for child in self.stack:
            child.attach(self.state, self._on_child_update)

    def detach(self):
        self._update_parent = None
        for child in self.stack:
            child.detach()

    def _refresh(self):
        if self._update_parent is not None:
            self._update_parent(self, DisplayUpdate.UPDATE, None)

    def _on_child_update(
        self,
        sender: Display,
        op: DisplayUpdate,
        new_display: Display | None,
    ):
        current_display = self._peek()
        if op == DisplayUpdate.PUSH:
            assert current_display is sender
            assert new_display is not None
            self._push(new_display)
        elif op == DisplayUpdate.POP:
            if current_display is sender:
                self._pop()
        elif op == DisplayUpdate.UPDATE:
            if current_display is sender:
                self._refresh()
