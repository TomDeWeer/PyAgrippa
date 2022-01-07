from enum import Enum


class HashDecision(Enum):
    CONTINUE = 1  # do nothing
    RETURN = 2  # use the hash move
    MOVE_REORDER = 3  # use hash move in move ordering
