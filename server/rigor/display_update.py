from enum import Enum


class DisplayUpdate(Enum):
    NONE = 0
    UPDATE = 1
    POP = 2
    PUSH = 3
    REPLACE = 4
