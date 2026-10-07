from enum import Enum

class BlockSize(Enum):
    BYTE = 1
    HALF_WORD = 2
    WORD = 4

class Effect(Enum):
    SET_BIT ="set_bit"
    ADD = "add"
    SET_VALUE = "set_value"
    TEMPORARY = "temporary"
    NONE = "none"
