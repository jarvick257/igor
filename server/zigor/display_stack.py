from typing import List

from .display import Display


class DisplayStack:
    def __init__(self):
        self.stack: List[Display] = []

    def push(self, display: Display) -> None:
        if len(self.stack) > 0:
            self.peek().disable()
        self.stack.append(display)
        self.peek().enable()

    def pop(self) -> None:
        assert len(self.stack) > 1
        self.peek().disable()
        self.stack = self.stack[:-1]
        self.peek().enable()

    def peek(self) -> Display:
        assert len(self.stack) > 0
        return self.stack[-1]
