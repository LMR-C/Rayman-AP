from enum import Enum


class BlockSize(Enum):
    BYTE = 1
    HALF_WORD = 2
    WORD = 4


class Effect(Enum):
    BIT = "bit"
    COUNTER = "counter"
    SET_VALUE = "set_value"
    RAISE_MAX = "raise_max"  # set a max, then refill the counter it bounds (e.g. Big Power)
    NONE = "none"
