from BaseClasses import Item, ItemClassification
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .utils import BlockSize, Effect
from .options import RaymanGameOptions

if TYPE_CHECKING:
    from .world import RaymanWorld

@dataclass(frozen=True)
class ItemData :
    id : int
    name : str
    address : tuple[int, ...]
    size: BlockSize
    mask: int
    count : int
    effect : Effect
    classification : ItemClassification
    value : int

class RaymanItem(Item) :
    game = "Rayman"

def get_item_table(options: RaymanGameOptions = None) -> tuple[ItemData, ...]:
    is_life_sanity = options is not None and options.include_life_status_in_location.value
    is_magician_sanity = options is not None and options.include_magician_challenges_in_location.value
    is_magic_seed = options is not None and options.magic_seed_as_item.value

    return (
        # Powers
        ItemData(1001, "Telescopic Fist", (0x1f43d0), BlockSize.BYTE, 0x1, 1, Effect.SET_BIT, ItemClassification.progression, None),
        ItemData(1002, "Hanging", (0x1f43d0), BlockSize.BYTE, 0x2, 1, Effect.SET_BIT, ItemClassification.progression, None),
        ItemData(1003, "Grappling Fist", (0x1f43d0), BlockSize.BYTE, 0x80, 1, Effect.SET_BIT, ItemClassification.progression, None),
        ItemData(1004, "Helicopter", (0x1f43d0), BlockSize.BYTE, 0x4, 1, Effect.SET_BIT, ItemClassification.progression, None),

        # Level Unlock
        ItemData(5001, "Anguish Lagoon Unlock", (0x1C3378), BlockSize.BYTE, None, 1, Effect.SET_VALUE, ItemClassification.progression, 3),
        ItemData(5002, "The Swamps of Forgetfulness Unlock", (0x1C3384), BlockSize.BYTE, None, 1, Effect.SET_VALUE, ItemClassification.progression, 3),
        ItemData(5003, "Moskito's Nest Unlock", (0x1C33A0), BlockSize.BYTE, None, 1, Effect.SET_VALUE, ItemClassification.progression, 3),

        # Special items
        ItemData(2001, "Magic Seed", (0x1f43d0), BlockSize.BYTE, 0x40, 1 if is_magic_seed else 0, Effect.SET_BIT, ItemClassification.progression, None),

        # Key items
        ItemData(3001, "Cage", (0x1F8138), BlockSize.BYTE, None, 24, Effect.ADD, ItemClassification.useful, 1),

        # Filler item
        ItemData(6001, "Simple Power", (0x1F6200), BlockSize.BYTE, None, None, Effect.ADD, ItemClassification.filler, 1),
        ItemData(6002, "Double Power", (0x1F6200), BlockSize.BYTE, None, None, Effect.ADD, ItemClassification.filler, 2),
        ItemData(6003, "Big Power", (0x1F6200, 0x1E4D59), BlockSize.BYTE, None, None, Effect.ADD, ItemClassification.filler, 5),
        ItemData(8001, "Life Status", (0x1E4D50), BlockSize.BYTE, None, 
                 (12 if is_life_sanity else 0) + (4 if is_magician_sanity else 0),
                 Effect.ADD, ItemClassification.filler, 1),
        ItemData(9001, "5 tings", (0x1E4D56), BlockSize.BYTE, None, 65 if is_life_sanity else None, Effect.ADD, ItemClassification.filler, 1),

        # Traps item
        ItemData(10001, "Reversed controls", (0x1f43d1), BlockSize.BYTE, 0x20, None, Effect.SET_BIT, ItemClassification.trap, None),
        ItemData(10002, "Forced Run", (0x1f43d1), BlockSize.BYTE, 0x10, None, Effect.SET_BIT, ItemClassification.trap, None),
    )

# Can be deleted if useless in the future
ITEM_NAME_TABLE = {item.name: item for item in get_item_table()}
ITEM_ID_TABLE = { item.id: item for item in get_item_table()}
# Needed for AP
ITEM_NAME_TO_ID = {item.name: item.id for item in get_item_table()}
