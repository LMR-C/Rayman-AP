from dataclasses import dataclass
from rule_builder.rules import Rule

from .options import RaymanGameOptions, Difficulty
from . import rules

@dataclass(frozen=True)
class EntranceData:
    name: str
    from_region: str
    to_region: str
    rule: Rule

def get_entrance_table(options: RaymanGameOptions = None) -> tuple[EntranceData, ...]:
    is_difficulty_normal = options.difficulty.value == Difficulty.option_normal
    is_magic_seed = options.magic_seed_as_item

    return (
        # Level entrances from worldmap
        EntranceData(
            name = "worldmap_to_ppw_s1",
            from_region = "worldmap",
            to_region = "Pink Plant Woods Screen 1",
            rule = rules.none
        ),
        EntranceData(
            name = "worldmap_to_al_s1",
            from_region = "worldmap",
            to_region = "Anguish Lagoon Screen 1",
            rule = rules.can_access_anguish_lagoon
        ),
        EntranceData(
            name = "worldmmap_to_sf_s1",
            from_region = "worldmap",
            to_region = "The Swamps of Forgetfulness Screen 1",
            rule = rules.can_access_swamps_of_forgetfulness
        ),
        EntranceData(
            name = "worldmap_to_mn_s1",
            from_region = "worldmap",
            to_region = "Moskito's Nest Screen 1",
            rule = rules.can_acess_moskito_nest
        ),

        # Back to worldmap from back signs
        EntranceData(
            name = "ppw_s1_to_worldmap",
            from_region = "Pink Plant Woods Screen 1",
            to_region = "worldmap",
            rule = rules.none
        ),
        EntranceData(
            name = "al_s1_to_worldmap",
            from_region = "Anguish Lagoon Screen 1",
            to_region = "worldmap",
            rule = rules.none
        ),
        EntranceData(
            name = "sf_s1_to_worldmap",
            from_region = "The Swamps of Forgetfulness Screen 1",
            to_region = "worldmap",
            rule = rules.none
        ),
        EntranceData(
            name = "mn_s1_to_worldmap",
            from_region = "Moskito's Nest Screen 1",
            to_region = "worldmap",
            rule = rules.none
        ),

        # Pink Plant Wood
        EntranceData(
            name = "ppw_s1_to_ppw_s2",
            from_region = "Pink Plant Woods Screen 1",
            to_region = "Pink Plant Woods Screen 2",
            rule = rules.none
        ),
        EntranceData(
            name = "ppw_s2_to_ppw_betilla",
            from_region = "Pink Plant Woods Screen 2",
            to_region = "Pink Plant Woods Betilla",
            rule = rules.none
        ),
        EntranceData(
            name = "ppw_betilla_to_ppw_s3",
            from_region = "Pink Plant Woods Betilla",
            to_region = "Pink Plant Woods Screen 3",
            rule = rules.has_fist | rules.has_hang
        ),
        EntranceData(
            name = "ppw_s3_to_worldmap",
            from_region = "Pink Plant Woods Screen 3",
            to_region = "worldmap",
            rule = rules.has_fist if is_difficulty_normal else rules.none
        ),
        
        # Anguish Lagoon
        EntranceData(
            name = "al_s1_to_al_s2",
            from_region = "Anguish Lagoon Screen 1",
            to_region = "Anguish Lagoon Screen 2",
            rule = rules.has_fist
        ),
        EntranceData(
            name = "al_s2_to_al_s3",
            from_region = "Anguish Lagoon Screen 2",
            to_region = "Anguish Lagoon Screen 3",
            rule = rules.has_fist
        ),
        EntranceData(
            name = "al_s3_to_al_betilla",
            from_region = "Anguish Lagoon Screen 3",
            to_region = "Anguish Lagoon Betilla",
            rule = rules.none
        ),
        EntranceData(
            name = "al_betilla_to_worldmap",
            from_region = "Anguish Lagoon Betilla",
            to_region = "worldmap",
            rule = rules.has_hang
        ),

        # The Swamps of Forgetfullness
        EntranceData(
            name = "sf_s1_to_sf_s2",
            from_region = "The Swamps of Forgetfulness Screen 1",
            to_region = "The Swamps of Forgetfulness Screen 2",
            rule = (rules.has_magic_seed & rules.has_fist if is_magic_seed else rules.has_fist) if is_difficulty_normal else (rules.has_magic_seed if is_magic_seed else rules.none)
        ),
        EntranceData(
            name = "sf_s2_to_sf_s3",
            from_region = "The Swamps of Forgetfulness Screen 2",
            to_region = "The Swamps of Forgetfulness Screen 3",
            rule = rules.has_fist if is_difficulty_normal else rules.none
        ),
        EntranceData(
            name = "sf_s3_to_worlmap",
            from_region = "The Swamps of Forgetfulness Screen 3",
            to_region = "worldmap",
            rule = rules.has_fist
        ),

        # Moskito's Nest
        EntranceData(
            name = "mn_s1_to_mn_s2",
            from_region = "Moskito's Nest Screen 1",
            to_region = "Moskito's Nest Screen 2",
            rule = rules.has_fist
        ),
        EntranceData(
            name = "mn_s2_to_mn_s3",
            from_region = "Moskito's Nest Screen 2",
            to_region = "Moskito's Nest Screen 3",
            rule = rules.none
        ),
        EntranceData(
            name = "mn_s3_to_mn_s4",
            from_region = "Moskito's Nest Screen 3",
            to_region = "Moskito's Nest Screen 4",
            rule = rules.none
        ),
        EntranceData(
            name = "mn_s4_to_mn_s5",
            from_region = "Moskito's Nest Screen 4",
            to_region = "Moskito's Nest Screen 5",
            rule = rules.none
        ),
        EntranceData(
            name = "mn_s5_to_mn_betilla",
            from_region = "Moskito's Nest Screen 5",
            to_region = "Moskito's Nest Betilla",
            rule = rules.has_fist
        ),
        EntranceData(
            name = "mn_betilla_to_worldmap",
            from_region = "Moskito's Nest Betilla",
            to_region = "worldmap",
            rule = rules.has_fist & rules.has_grappling_fist
        )
    )
