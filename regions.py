from dataclasses import dataclass

@dataclass(frozen=True)
class RegionData:
    name: str

REGIONS: tuple[RegionData, ...] = (
    RegionData(name="worldmap"),
    RegionData(name="Pink Plant Woods Screen 1"),
    RegionData(name="Pink Plant Woods Screen 2"),
    RegionData(name="Pink Plant Woods Betilla"),
    RegionData(name="Pink Plant Woods Screen 3"),
    RegionData(name="Anguish Lagoon Screen 1"),
    RegionData(name="Anguish Lagoon Screen 2"),
    RegionData(name="Anguish Lagoon Screen 3"),
    RegionData(name="Anguish Lagoon Betilla"),
    RegionData(name="The Swamps of Forgetfulness Screen 1"),
    RegionData(name="The Swamps of Forgetfulness Screen 2"),
    RegionData(name="The Swamps of Forgetfulness Screen 3"),
    RegionData(name="Moskito's Nest Screen 1"),
    RegionData(name="Moskito's Nest Screen 2"),
    RegionData(name="Moskito's Nest Screen 3"),
    RegionData(name="Moskito's Nest Screen 4"),
    RegionData(name="Moskito's Nest Screen 5"),
    RegionData(name="Moskito's Nest Betilla"),
)

LEVEL_ORDER_BY_REGION = {
    "Pink Plant Woods Screen 1": 1,
    "Pink Plant Woods Screen 2": 1,
    "Pink Plant Woods Betilla": 1,
    "Pink Plant Woods Screen 3": 1,

    "Anguish Lagoon Screen 1": 2,
    "Anguish Lagoon Screen 2": 2,
    "Anguish Lagoon Screen 3": 2,
    "Anguish Lagoon Betilla": 2,

    "The Swamps of Forgetfulness Screen 1": 3,
    "The Swamps of Forgetfulness Screen 2": 3,
    "The Swamps of Forgetfulness Screen 3": 3,

    "Moskito's Nest Screen 1": 4,
    "Moskito's Nest Screen 2": 4,
    "Moskito's Nest Screen 3": 4,
    "Moskito's Nest Screen 4": 4,
    "Moskito's Nest Screen 5": 4,
    "Moskito's Nest Betilla": 4,
}

UNLOCK_ITEM_ORDER = {
    "Anguish Lagoon Unlock": 2,
    "The Swamps of Forgetfulness Unlock": 3,
    "Moskito's Nest Unlock": 4,
}
