from dataclasses import dataclass

from BaseClasses import Location, LocationProgressType, Region
from rule_builder.rules import Rule

from .utils import BlockSize
from .options import RaymanGameOptions, Difficulty
from . import rules


@dataclass(frozen=True)
class LocationData :
    id : int
    name : str
    address : int
    size : BlockSize
    mask : int
    world_id : int
    level_id : int
    region : str
    rule : Rule
    classification : LocationProgressType

class RaymanLocation(Location):
    game="Rayman"

    def __init__(self, player: int, data: LocationData, parent: Region):
        super().__init__(
            player,
            data.name,
            data.id,
            parent,
        )

        self.progress_type = data.classification

        self.memory_address = data.address
        self.size = data.size
        self.mask = data.mask
        self.world_id = data.world_id
        self.level_id = data.level_id


def get_location_table(options: RaymanGameOptions = None) -> tuple[LocationData, ...]:

    # pre-process of options condition
    is_difficulty_normal = options is not None and options.difficulty.value == Difficulty.option_normal
    is_magic_seed = options is not None and options.magic_seed_as_item.value

    return (
        LocationData(
            2001, "Betilla Gift 1 (fist)", 0x1f43d0, BlockSize.BYTE, 0x1, 1, 3,
            "Pink Plant Woods Betilla", rules.none, LocationProgressType.PRIORITY
        ),
        LocationData(
            2002, "Betilla Gift 2 (hang)", 0x1F43D0, BlockSize.BYTE, 0x2, 1, 8,
            "Anguish Lagoon Betilla", rules.none, LocationProgressType.PRIORITY
        ),
        LocationData(
            2003, "Betilla Gift 3 (grappling fist)", 0x1F43D0, BlockSize.BYTE, 0x80, 1, 17,
            "Moskito's Nest Betilla", rules.none, LocationProgressType.PRIORITY
        ),
        LocationData(
            3001, "Moskito 1", 0x1F4EE8, BlockSize.BYTE, 0x1, 1, 6,
            "Anguish Lagoon Screen 2", rules.has_fist, LocationProgressType.PRIORITY
        ),
        LocationData(
            3002, "Moskito 2", 0x1F4EE8, BlockSize.BYTE, 0x2, 1, 16,
            "Moskito's Nest Screen 5", rules.has_fist, LocationProgressType.PRIORITY
        ),
        LocationData(
            7001, "Pink Plant Woods finished", 0x1C3378, BlockSize.BYTE, 0x3, 1, 4,
            "Pink Plant Woods Screen 3",
            rules.has_fist if is_difficulty_normal else rules.none,
            LocationProgressType.DEFAULT
        ),
        LocationData(
            7002, "Anguish Lagoon finished", 0x1C3384, BlockSize.BYTE, 0x3, 1, 8,
            "Anguish Lagoon Betilla",
            rules.has_hang,
            LocationProgressType.DEFAULT
        ),
        LocationData(
            7003, "The Swamps of Forgetfulness finished", 0x1C33A0, BlockSize.BYTE, 0x3, 1, 11,
            "The Swamps of Forgetfulness Screen 3",
            rules.has_fist,
            LocationProgressType.DEFAULT
        ),
        LocationData(
            4001, "Pink Plant Woods Screen 1 life 1", 0x1F9AC8, BlockSize.BYTE, 0x80, 1, 1,
            "Pink Plant Woods Screen 1", rules.none, LocationProgressType.DEFAULT
        ),
        LocationData(
            4002, "Pink Plant Woods Screen 2 life 1", 0x1F9AE9, BlockSize.BYTE, 0x80, 1, 2,
            "Pink Plant Woods Screen 2", rules.none, LocationProgressType.DEFAULT
        ),
        LocationData(
            4003, "Pink Plant Woods Screen 2 life 2", 0x1F9AE9, BlockSize.BYTE, 0x40, 1, 2,
            "Pink Plant Woods Screen 2", rules.has_hang, LocationProgressType.DEFAULT
        ),
        LocationData(
            1001, "Pink Plant Woods Screen 2 cage 1", 0x1F9AF1, BlockSize.BYTE, 0x20, 1, 2,
            "Pink Plant Woods Screen 2", rules.has_fist & rules.has_hang, LocationProgressType.DEFAULT
        ),
        LocationData(
            1002, "Pink Plant Woods Screen 2 cage 2", 0x1F9AF1, BlockSize.BYTE, 0x10, 1, 2,
            "Pink Plant Woods Screen 2", rules.has_fist & rules.has_hang, LocationProgressType.DEFAULT
        ),
        LocationData(
            1003, "Pink Plant Woods Screen 2 cage 3", 0x1F9AF1, BlockSize.BYTE, 0x4, 1, 2,
            "Pink Plant Woods Screen 2", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            5001, "Pink Plant Woods Screen 2 magician 1", 0x1f7f40, BlockSize.WORD, 0x00100000, 1, 2,
            "Pink Plant Woods Screen 2", rules.none, LocationProgressType.DEFAULT
        ),
        LocationData(
            4004, "Pink Plant Woods Screen 3 life 1", 0x1F9B28, BlockSize.BYTE, 0x80, 1, 4,
            "Pink Plant Woods Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            4005, "Pink Plant Woods Screen 3 life 2", 0x1F9B28, BlockSize.BYTE, 0x40, 1, 4,
            "Pink Plant Woods Screen 3", rules.none, LocationProgressType.DEFAULT
        ),
        LocationData(
            4006, "Pink Plant Woods Screen 3 life 3", 0x1F9B2A, BlockSize.BYTE, 0x20, 1, 4,
            "Pink Plant Woods Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            4007, "Pink Plant Woods Screen 3 life 4", 0x1F9B2A, BlockSize.BYTE, 0x4, 1, 4,
            "Pink Plant Woods Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            4008, "Pink Plant Woods Screen 3 life 5", 0x1F9B28, BlockSize.BYTE, 0x10, 1, 4,
            "Pink Plant Woods Screen 3", rules.none, LocationProgressType.DEFAULT
        ),
        LocationData(
            1004, "Pink Plant Woods Screen 3 cage 1", 0x1F9B31, BlockSize.HALF_WORD, 0x2000, 1, 4,
            "Pink Plant Woods Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1005, "Pink Plant Woods Screen 3 cage 2", 0x1F9B31, BlockSize.HALF_WORD, 0x01, 1, 4,
            "Pink Plant Woods Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1006, "Pink Plant Woods Screen 3 cage 3", 0x1F9B31, BlockSize.HALF_WORD, 0x8000, 1, 4,
            "Pink Plant Woods Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            5002, "Pink Plant Woods Screen 3 magician 1", 0x1f7f40, BlockSize.WORD, 0x80000, 1, 4,
            "Pink Plant Woods Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1007, "Anguish Lagoon Screen 1 cage 1", 0x1F9B4C, BlockSize.BYTE, 0x20, 1, 5,
            "Anguish Lagoon Screen 1", rules.has_fist & (rules.has_helicopter | rules.has_grappling_fist), LocationProgressType.DEFAULT
        ),
        LocationData(
            1008, "Anguish Lagoon Screen 1 cage 2", 0x1F9B4C, BlockSize.BYTE, 0x40, 1, 5,
            "Anguish Lagoon Screen 1", rules.has_fist & rules.has_grappling_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1009, "Anguish Lagoon Screen 1 cage 3", 0x1F9B4B, BlockSize.HALF_WORD, 0x1, 1, 5,
            "Anguish Lagoon Screen 1", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1010, "Anguish Lagoon Screen 1 cage 4", 0x1F9B4B, BlockSize.HALF_WORD, 0x8000, 1, 5,
            "Anguish Lagoon Screen 1", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1011, "Anguish Lagoon Screen 1 cage 5", 0x1F9B4C, BlockSize.BYTE, 0x8, 1, 5,
            "Anguish Lagoon Screen 1", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            4009, "Anguish Lagoon Screen 1 life 1", 0x1F9B4A, BlockSize.BYTE, 0x10, 1, 5,
            "Anguish Lagoon Screen 1", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            4010, "Anguish Lagoon Screen 3 life 1", 0x1F9B92, BlockSize.BYTE, 0x4, 1, 7,
            "Anguish Lagoon Screen 3", rules.none, LocationProgressType.DEFAULT
        ),
        LocationData(
            4011, "Anguish Lagoon Screen 3 life 2", 0xAF9B93, BlockSize.BYTE, 0x2, 1, 7,
            "Anguish Lagoon Screen 3", rules.none, LocationProgressType.DEFAULT
        ),
        LocationData(
            1012, "Anguish Lagoon Screen 3 cage 1", 0x1F9B8B, BlockSize.BYTE, 0x40, 1, 7,
            "Anguish Lagoon Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1013, "The Swamps of Forgetfulness Screen 1 cage 1", 0x1F9BC8, BlockSize.BYTE, 0x10, 1, 9,
            "The Swamps of Forgetfulness Screen 1", 
            rules.has_fist & rules.has_magic_seed if is_magic_seed else rules.has_fist,
            LocationProgressType.DEFAULT
        ),
        LocationData(
            1014, "The Swamps of Forgetfulness Screen 1 cage 2", 0x1F9BCA, BlockSize.BYTE, 0x20, 1, 9,
            "The Swamps of Forgetfulness Screen 1",
            rules.has_fist & rules.has_magic_seed if is_magic_seed else rules.has_fist,
            LocationProgressType.DEFAULT
        ),
        LocationData(
            4012, "The Swamps of Forgetfulness Screen 1 life 1", 0x1F9BCA, BlockSize.BYTE, 0x8, 1, 9,
            "The Swamps of Forgetfulness Screen 1",
            rules.has_fist & rules.has_magic_seed if is_magic_seed else rules.has_fist,
            LocationProgressType.DEFAULT
        ),
        LocationData(
            1015, "The Swamps of Forgetfulness Screen 2 cage 1", 0x1F9BEE, BlockSize.HALF_WORD, 0x2, 1, 10,
            "The Swamps of Forgetfulness Screen 2", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1016, "The Swamps of Forgetfulness Screen 2 cage 2", 0x1F9BEE, BlockSize.HALF_WORD, 0x800, 1, 10,
            "The Swamps of Forgetfulness Screen 2", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1017, "The Swamps of Forgetfulness Screen 3 cage 1", 0x1F9C10, BlockSize.BYTE, 0x4, 1, 11,
            "The Swamps of Forgetfulness Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1018, "The Swamps of Forgetfulness Screen 3 cage 2", 0x1F9C10, BlockSize.BYTE, 0x2, 1, 11,
            "The Swamps of Forgetfulness Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            5003, "The Swamps of Forgetfulness Screen 3 magician 1", 0x1f7f40, BlockSize.WORD, 0x20000, 1, 11,
            "The Swamps of Forgetfulness Screen 3", rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1019, "Moskito's Nest Screen 1 cage 1", 0x1F9C2F, BlockSize.BYTE, 0x40, 1, 12,
            "Moskito's Nest Screen 1",
            rules.has_fist & rules.has_hang & rules.has_grappling_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1020, "Moskito's Nest Screen 1 cage 2", 0x1F9C2F, BlockSize.BYTE, 0x8, 1, 12,
            "Moskito's Nest Screen 1",
            rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1021, "Moskito's Nest Screen 1 cage 3", 0x1F9C2F, BlockSize.BYTE, 0x4, 1, 12,
            "Moskito's Nest Screen 1",
            rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            5004, "Moskito's Nest Screen 1 magician 1", 0x1f7f40, BlockSize.WORD, 0x40000, 1, 12,
            "Moskito's Nest Screen 1",
            rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1022, "Moskito's Nest Screen 2 cage 1", 0x1F9C51, BlockSize.BYTE, 0x8, 1, 13,
            "Moskito's Nest Screen 2",
            rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1023, "Moskito's Nest Screen 2 cage 2", 0x1F9C51, BlockSize.BYTE, 0x2, 1, 13,
            "Moskito's Nest Screen 2",
            rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            1024, "Moskito's Nest Screen 2 cage 3", 0x1F9C51, BlockSize.BYTE, 0x1, 1, 13,
            "Moskito's Nest Screen 2",
            rules.has_fist, LocationProgressType.DEFAULT
        ),
        LocationData(
            4013, "Moskito's Nest Screen 4 life 1", 0x1F9C8D, BlockSize.BYTE, 0x2, 1, 15,
            "Moskito's Nest Screen 4",
            rules.has_fist & rules.has_grappling_fist, LocationProgressType.DEFAULT
        ),
    )

# Can be deleted if useless in the future
LOCATION_NAME_TABLE = {loc.name: loc for loc in get_location_table()}
LOCATION_ID_TABLE = {loc.id : loc for loc in get_location_table()}
# Needed for AP
LOCATION_NAME_TO_ID = {loc.name: loc.id for loc in get_location_table()}
