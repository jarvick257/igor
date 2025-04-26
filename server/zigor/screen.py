from typing import TypeVar, Generic, Any, Optional, Callable
from .encoder import EncoderAction
from .content import Content
from .display_update import DisplayUpdate
from .display import Display

T = TypeVar("T")


class Screen(Generic[T], Display):
    def __init__(self):
        self._state: T | None
        self._update_parent: (
            Callable[["Display", DisplayUpdate, Optional["Display"]], None] | None
        )

    @property
    def state(self) -> T:
        assert (
            self._state is not None
        ), "Can't access state before being attached to stack"
        assert self._update_parent is not None
        return self._state

    def attach(
        self,
        state: Any,
        callback: Callable[["Display", DisplayUpdate, Optional["Display"]], None],
    ) -> None:
        self._state = state
        self._update_parent = callback
        self.on_attach()

    def detach(self):
        self._update_parent = None
        self._state = None
        self.on_detach()

    def on_attach(self):
        pass

    def on_detach(self):
        pass

    def on_input(self, action: EncoderAction) -> None:
        if action == EncoderAction.NONE:
            self.on_nop()
        elif action == EncoderAction.ENTER:
            self.on_enter()
        elif action == EncoderAction.NEXT:
            self.on_next()
        elif action == EncoderAction.PREV:
            self.on_prev()

    def on_nop(self) -> None:
        pass

    def on_enter(self) -> None:
        pass

    def on_next(self) -> None:
        pass

    def on_prev(self) -> None:
        pass

    def render(self) -> Content:
        raise NotImplementedError()

    def pop(self):
        assert self._update_parent is not None
        self._update_parent(self, DisplayUpdate.POP, None)

    def push(self, display: Display):
        assert self._update_parent is not None
        self._update_parent(self, DisplayUpdate.PUSH, display)

    def refresh(self):
        assert self._update_parent is not None
        self._update_parent(self, DisplayUpdate.UPDATE, None)
