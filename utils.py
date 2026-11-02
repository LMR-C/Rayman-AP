from enum import Enum


class BlockSize(Enum):
    BYTE = 1
    HALF_WORD = 2
    WORD = 4

class Effect(Enum):
    BIT ="bit"
    COUNTER = "counter"
    NONE = "none"
