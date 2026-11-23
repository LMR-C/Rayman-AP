from dataclasses import dataclass

from Options import Choice, DeathLink, OptionGroup, PerGameCommonOptions, Range, Toggle


class NumberOfStartingLife(Range):
    """
    The base number of life
    """

    display_name = "Number of starting life"
    range_start = 0
    range_end = 99
    default = 3


class NumberOfContinue(Range):
    """
    The base number of continue available when you loose all your lives
    """

    display_name = "Number of continues"
    range_start = 0
    range_end = 99
    default = 5


class NumberOfTingsToGetANewLife(Range):
    """
    The number of tings to get in order to obtain a new life
    """

    display_name = "Number of tings to get a new life"
    range_start = 50
    range_end = 100
    default = 100


class Difficulty(Choice):
    """
    Let you choose the difficulty of you playthrough

    Normal : Casual playthrough for progression, don't require damage boos, speedrun tricks or other
    tricky moves to get the checks

    Hard : progression and checks may require speedrun tricks, damage boost and other tricky moves
    """

    display_name = "Difficulty"
    option_normal = 0
    option_hard = 1


class Goal(Choice):
    """
    Let you choose what goal to achieve in order to finish the game

    Defeat Mr.Dark : Defeat Mr.Dark to save the Rayman's world !
    """

    display_name = "Goal"
    option_cages = 0

class NumberOfRequiredCages(Range):
    """
    The number of cages required to unlock Mr.Dark's Dare
    """

    display_name = "Number of tings to get a new life"
    range_start = 25
    range_end = 102
    default = 102


class TrapFillPercentage(Range):
    """
    The percentage of filler items to replace by traps
    """

    display_name = "Trap fill percentage"
    range_start = 0
    range_end = 100
    default = 0


class ReversedControlsWeight(Choice):
    """
    The likelyhood of receiving a trap wich reverses controls
    """

    display_name = "Reversed Controls weight"
    option_none = 0
    option_low = 1
    option_medium = 1.5
    option_high = 1.75


class ForcedRunWeight(Choice):
    """
    The likelyhood of receiving a trap wich forces Rayman to run
    """

    display_name = "Forced Run weight"
    option_none = 0
    option_low = 1
    option_medium = 1.5
    option_high = 1.75


class MagicSeedAsItem(Toggle):
    """
    If active: you need to find the magic seed in order to use it in The Swamps of Forgetfulness
    """

    display_name = "Magic Seed as item"

class SuperHelicopterPotionAsItem(Toggle):
    """
    If active: you need to find the Super Helicopter Potion in order to use it in the Mr.Stone's Peaks
    """

    display_name = "Super Helicopter Potion as item"

class FireflyAsItem(Toggle):
    """
    If active: you need to find the Firefly in order to use it in Eat at Joe's
    """

    display_name = "Firefly as item"


class IncludeLifeStatusInLocation(Toggle):
    """
    Life status count as location checks
    """

    display_name = "Include life status in location checks"


class IncludeMagicianChallengeInLocation(Toggle):
    """
    Magician challenges count as checks
    """

    display_name = "Include Magician challenges in location checks"

class SimplePowerWeight(Choice):
    """
    The likelyhood of receiving a Simple Power as filler item
    """

    display_name = "Simple Power weight"
    option_none = 0
    option_low = 0.5
    option_medium = 1
    option_high = 1.5

class DoublePowerWeight(Choice):
    """
    The likelyhood of receiving a Double Power as filler item
    """

    display_name = "Double Power weight"
    option_none = 0
    option_low = 0.5
    option_medium = 1
    option_high = 1.5

class BigPowerWeight(Choice):
    """
    The likelyhood of receiving a Big Power as filler item
    """

    display_name = "Big Power weight"
    option_none = 0
    option_low = 0.5
    option_medium = 1
    option_high = 1.5

class LifeStatuesWeight(Choice):
    """
    The likelyhood of receiving a Life Statue as filler item
    """

    display_name = "Life statue weight"
    option_none = 0
    option_low = 0.5
    option_medium = 1
    option_high = 1.5

class TingsWeight(Choice):
    """
    The likelyhood of receiving a 5 tings as filler item
    """

    display_name = "5 tings weight"
    option_none = 0
    option_low = 0.5
    option_medium = 1
    option_high = 1.5


rayman_options_groups = [
    OptionGroup("Quality of life", [NumberOfStartingLife, NumberOfContinue, NumberOfTingsToGetANewLife]),
    OptionGroup("General Options", [Difficulty, NumberOfRequiredCages]),
    OptionGroup("Item Options", [
        TrapFillPercentage,
        ReversedControlsWeight,
        ForcedRunWeight,
        MagicSeedAsItem,
        SuperHelicopterPotionAsItem,
        FireflyAsItem,
        SimplePowerWeight,
        DoublePowerWeight,
        BigPowerWeight,
        LifeStatuesWeight,
        TingsWeight
    ]),
    OptionGroup(
        "Location Options",
        [
            IncludeLifeStatusInLocation,
            IncludeMagicianChallengeInLocation,
        ],
    ),
]


@dataclass
class RaymanGameOptions(PerGameCommonOptions):
    death_link: DeathLink
    number_of_starting_life: NumberOfStartingLife
    number_of_continue: NumberOfContinue
    number_of_tings_to_get_a_new_life: NumberOfTingsToGetANewLife
    difficulty: Difficulty
    number_of_required_cage: NumberOfRequiredCages
    trap_fill_percentage: TrapFillPercentage
    reversed_controls_weight: ReversedControlsWeight
    forced_run_weight: ForcedRunWeight
    magic_seed_as_item: MagicSeedAsItem
    super_helicopter_potion_as_item: SuperHelicopterPotionAsItem
    firefly_as_item: FireflyAsItem
    include_life_status_in_location: IncludeLifeStatusInLocation
    include_magician_challenges_in_location: IncludeMagicianChallengeInLocation
    simple_power_weight: SimplePowerWeight
    double_power_weight: DoublePowerWeight
    big_power_weight: BigPowerWeight
    life_statue_weight: LifeStatuesWeight
    tings_weight: TingsWeight
