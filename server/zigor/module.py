from typing import Callable, Any, Optional, TypeVar, Generic, List

from .content import Content
from .display_update import DisplayUpdate
from .encoder import EncoderAction

from .interfaces import IDisplay

T = TypeVar("T")


class Module(Generic[T], IDisplay):
    def __init__(self, module_state: T, display: IDisplay):
        self.state: T = module_state
        self.stack: List[IDisplay] = []
        self._update_parent = None
        self._push(display)

    def _push(self, display: IDisplay) -> None:
        self.stack.append(display)
        if self._update_parent is not None:
            display.register(self.state, self._on_child_update)
            self._refresh()

    def _pop(self) -> None:
        if len(self.stack) > 1:
            self.stack[-1].unregister()
            self.stack = self.stack[:-1]
            self._refresh()
        elif self._update_parent:
            self._update_parent(self, DisplayUpdate.POP, None)

    def _peek(self) -> IDisplay:
        assert len(self.stack) > 0
        return self.stack[-1]

    def on_input(self, action: EncoderAction) -> None:
        self._peek().on_input(action)

    def render(self) -> Content:
        return self._peek().render()

    def register(
        self,
        state: Any,
        callback: Callable[["IDisplay", DisplayUpdate, Optional["IDisplay"]], None],
    ) -> None:
        _ = state
        self._update_parent = callback
        for child in self.stack:
            child.register(self.state, self._on_child_update)

    def unregister(self):
        self._update_parent = None
        for child in self.stack:
            child.unregister()

    def _refresh(self):
        if self._update_parent is not None:
            self._update_parent(self, DisplayUpdate.UPDATE, None)

    def _on_child_update(
        self,
        sender: IDisplay,
        op: DisplayUpdate,
        new_display: IDisplay | None,
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
