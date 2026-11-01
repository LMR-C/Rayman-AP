from enum import Enum


class BlockSize(Enum):
    BYTE = 1
    HALF_WORD = 2
    WORD = 4

class Effect(Enum):
    BIT = "bit"          # flag(s) in a bitfield, idempotent
    COUNTER = "counter"  # +value on a counter, not idempotent
    NONE = "none"        # no RAM effect (filler)
