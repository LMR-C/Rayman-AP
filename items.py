from dataclasses import dataclass
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .utils import BlockSize, Effect

if TYPE_CHECKING:
    from .world import RaymanWorld

@dataclass(frozen=True)
class ItemData :
    name : str
    id : int
    classification : ItemClassification
    count : int #To see with model
    effect : Effect
    size: BlockSize = BlockSize.BYTE
    address : int  | None = None
    value : int = 0 # BIT: mask of the flag(s) / COUNTER: amount added

    def __post_init__(self) -> None:
        if self.effect is Effect.NONE:
            return
        if self.address is None:
            raise ValueError(f"Item {self.name!r}: effect {self.effect} needs an address")
        if self.value == 0:
            raise ValueError(f"Item {self.name!r}: effect {self.effect} needs a non-zero value")

class RaymanItem(Item) :
    game = "Rayman"


ITEMS = [
    ItemData("Fist Power", 1001, ItemClassification.progression,1,Effect.BIT,BlockSize.BYTE,0X1F43D0,0X01),
    ItemData("Hanging", 1002, ItemClassification.progression,1,Effect.BIT,BlockSize.BYTE,0X1F43D0,0X02),
    ItemData("Cage", 3001, ItemClassification.progression,1,Effect.COUNTER,BlockSize.BYTE,0x1F8138,1),
    ItemData("Life", 8001, ItemClassification.useful,1,Effect.COUNTER,BlockSize.BYTE,0x1E4D50,1),
    ItemData("Nothing", 2, ItemClassification.filler, 0, Effect.NONE)
]

def create_item_with_table(world : "RaymanWorld", name : str) -> RaymanItem :
    data = ITEM_NAME_TABLE[name]
    return RaymanItem(data.name,data.classification,data.id,world.player)

# Can be deleted if useless in the future
ITEM_NAME_TABLE = {item.name: item for item in ITEMS}
ITEM_ID_TABLE = { item.id: item for item in ITEMS}
# Needed for AP
ITEM_NAME_TO_ID = {item.name: item.id for item in ITEMS}

def create_available_items(world : "RaymanWorld") -> list[Item] :
    #Creating items needed on game
    item_pool : list[Item] = []
    for data in ITEMS:
        item_pool.extend(world.create_item(data.name) for _ in range(data.count))
    return item_pool


# Prototype : fixed placement to always get a playable seed (location name -> item name)
FORCED_PLACEMENT = {
    "Pink Plant Woods, screen 1, life 1": "Fist Power",
    "Pink Plant Woods, screen 2, life 1": "Hanging",
    "Pink Plant Woods, screen 2, cage 1": "Cage",
    "Pink Plant Woods, screen 2, cage 2": "Life",
}

def place_forced_items(world : "RaymanWorld") -> None :
    # Locked items must not be added to the item pool
    for location_name, item_name in FORCED_PLACEMENT.items():
        world.get_location(location_name).place_locked_item(world.create_item(item_name))


def create_all_items(world : "RaymanWorld") -> None :
    place_forced_items(world)
    placed_items = set(FORCED_PLACEMENT.values())
    item_pool = [item for item in create_available_items(world) if item.name not in placed_items]

    number_available_items = len(item_pool)
    number_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_filler_items = number_unfilled_locations - number_available_items

    item_pool+= [world.create_filler() for _ in range (needed_number_filler_items)]

    world.multiworld.itempool+=item_pool


def get_filler_item_name() -> str :
    # To change later
    return "Nothing"
