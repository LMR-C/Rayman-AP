from .utils import BlockSize, Effect
from dataclasses import dataclass
from BaseClasses import Item
from BaseClasses import ItemClassification
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import RaymanWorld

@dataclass(frozen=True)
class ItemData :
    name : str
    id : int
    classification : ItemClassification
    count : int #To see with model
    effect : Effect
    address : int  | None = None
    value : int = 0

class RaymanItem(Item) :
    game = "Rayman"


ITEMS = [
    ItemData("Fist Power", 1, ItemClassification.progression,1,Effect.SET_BIT,0X1F43D0,0X01),
    ItemData("Nothing", 2, ItemClassification.filler, 0, Effect.NONE)
]

def create_item_with_table(world : "RaymanWorld", name : str) -> RaymanItem :
    data = ITEM_TABLE[name]
    return RaymanItem(data.name,data.classification,data.id,world.player)

# Can be deleted if useless in the future
ITEM_TABLE = {item.name: item for item in ITEMS}
# Needed for AP
ITEM_NAME_TO_ID = {item.name: item.id for item in ITEMS}

def create_available_items(world : "RaymanWorld") -> list[Item] :
    #Creating items needed on game
    item_pool : list[Item] = []
    for data in ITEMS:
        if data.count >= 1:
            for _ in range(data.count):
                item_pool.append(world.create_item(data.name))
    return item_pool


def create_all_items(world : "RaymanWorld") -> None :
    item_pool = create_available_items(world)
    
    number_available_items = len(item_pool)
    number_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_filler_items = number_unfilled_locations - number_available_items
    
    item_pool+= [world.create_filler() for _ in range (needed_number_filler_items)]
    
    world.multiworld.itempool+=item_pool


def get_filler_item_name() -> str :
    # To change later
    return "Nothing"
