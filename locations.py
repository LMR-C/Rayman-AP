from .utils import BlockSize
from dataclasses import dataclass
from BaseClasses import Location

@dataclass(frozen=True)
class LocationData :
    name : str
    id : int
    region : str
    address : int
    mask : int
    size : BlockSize
    requires : tuple[str,...] =()

class RaymanLocation(Location):
    game="Rayman"

LOCATIONS = [
    LocationData("Pink Plant Woods, screen1, life 1", 1,"Pink Plant Woods",0x1F9AC8, 0X80, BlockSize.BYTE)
]

# Can be deleted if useless in the future
LOCATION_NAME_TABLE = {loc.name: loc for loc in LOCATIONS}
LOCATION_ID_TABLE = {loc.id : loc for loc in LOCATIONS}
# Needed for AP
LOCATION_NAME_TO_ID = {loc.name: loc.id for loc in LOCATIONS}


