from dataclasses import dataclass

from BaseClasses import Location

from .utils import BlockSize


@dataclass(frozen=True)
class LocationData :
    name : str
    id : int
    region : str
    address : int
    mask : int
    size : BlockSize
    requires : tuple[str,...] =()
    vanilla_item_id : int | None = None # item given by the game when the location is checked (reversed by the client)

class RaymanLocation(Location):
    game="Rayman"


LOCATIONS = [
    LocationData("Pink Plant Woods, screen 1, life 1", 4001,"Pink Plant Woods",0x1F9AC8, 0X80, BlockSize.BYTE, vanilla_item_id=8001),
    LocationData("Pink Plant Woods, screen 2, life 1", 4002,"Pink Plant Woods",0x1F9AE9, 0X80, BlockSize.BYTE, vanilla_item_id=8001),
    # has hang
    LocationData("Pink Plant Woods, screen 2, cage 1", 1001,"Pink Plant Woods",0x1F9AF1, 0X20, BlockSize.BYTE, vanilla_item_id=3001),
    # has fist and hang
    LocationData("Pink Plant Woods, screen 2, cage 2", 1002,"Pink Plant Woods",0x1F9AF1, 0X10, BlockSize.BYTE, vanilla_item_id=3001)
]

# Can be deleted if useless in the future
LOCATION_NAME_TABLE = {loc.name: loc for loc in LOCATIONS}
LOCATION_ID_TABLE = {loc.id : loc for loc in LOCATIONS}
# Needed for AP
LOCATION_NAME_TO_ID = {loc.name: loc.id for loc in LOCATIONS}


