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
