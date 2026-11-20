import time
from collections.abc import Callable
from dataclasses import dataclass

from .ram_map import (
    BETILLA_GIFT_1_LOCATION_ID,
    BETILLA_GIFT_2_LOCATION_ID,
    BETILLA_GIFT_3_LOCATION_ID,
    FORCED_RUN_ITEM_ID,
    GRAPPLING_FIST_ITEM_ID,
    HANGING_ITEM_ID,
    MAGIC_SEED_ITEM_ID,
    MAGIC_SEED_TEXT_1_ADDRESS,
    MAGIC_SEED_TEXT_1_ORIGINAL,
    MAGIC_SEED_TEXT_1_REPLACEMENT,
    MAGIC_SEED_TEXT_2_ADDRESS,
    MAGIC_SEED_TEXT_2_ORIGINAL,
    MAGIC_SEED_TEXT_2_REPLACEMENT,
    REVERSED_CONTROL_ITEM_ID,
    TELESCOPIC_FIST_ITEM_ID,
)
from .ram_operation import MaskOperation, RamOperation, ReplaceIfOperation, SetOperation

PREVIOUS_CONTINUE = 5


@dataclass(frozen=True)
class TrapState:
    seen: int = 0
    queue: tuple[int, ...] = ()
    active: int | None = None
    remaining_s: float = 0.0


NO_TRAPS = TrapState()  # default trap state (TrapState is frozen, so one shared instance is safe)


@dataclass(frozen=True)
class TickContext:
    """Snapshot of the game and the server for one tick, taken from the first read."""

    state: dict[str, int]  # STATE_READS (world, level, x, y, menu, ...)
    received: frozenset[int]  # ids of the received items
    missing: frozenset[int]  # locations not checked yet
    location_bits: dict[int, bool]  # bit read for each missing location (first read)
    slot_data: dict
    received_order: tuple[int, ...] = ()
    death_link_pending: bool = False  # DeathLink received, not applied in game yet


@dataclass(frozen=True)
class TickPlan:
    """What the special events decided for one tick, applied by the client and the builder."""

    banned_locations: frozenset[int]  # not sent to the server this tick
    forced_on: frozenset[int]  # items whose bit is set without being received
    forward_cut: frozenset[int]  # received items not given again this tick
    to_clear: frozenset[int]  # items whose bit is put back to 0
    armed: frozenset[int]  # armed locations, kept for the next tick
    raw_ops: tuple[tuple[int, RamOperation], ...] = ()  # (address, operation), tied to no item or location
    traps: TrapState = TrapState()


@dataclass(frozen=True)
class ForceWindow:
    """Set the bit of an item that is not received while ``active`` is true.

    Out of the window, the bit is cleared if the item is still not received and its location
    is not missing. Used to skip a Betilla scene when the location is already checked.

    Attributes:
        item_id: Item whose bit is forced.
        active: Whether the window is open this tick.
        location_id: Location tied to the item, None if it has none.
    """

    item_id: int
    active: Callable[[TickContext], bool]
    location_id: int | None = None  # location tied to the item (None for an item without location)


@dataclass(frozen=True)
class GatedLocation:
    """Protect a missing location detected on the bit of an item already received.

    A set bit may come from the client, so the location stays banned. In the zone, the forward is cut
    and the bit cleared; once the bit is read at 0 the location is armed, and the next set bit can only
    come from the game, so it counts as a real check. Leaving the zone disarms the location.

    Attributes:
        location_id: Location to protect.
        item_id: Item whose bit also detects the location.
        in_zone: Whether Rayman is where the item must be removed for the game to give it.
    """

    location_id: int
    item_id: int
    in_zone: Callable[[TickContext], bool]


@dataclass(frozen=True)
class FreeOperation:
    """A free operation executed if condition is true

    Attributes:
        condition: the condition to verify
        op: the ram operation(s) to apply
    """

    condition: Callable[[TickContext], bool]
    op: Callable[[TickContext], list[RamOperation]]


@dataclass(frozen=True)
class RemoveWindow:
    """Stop giving an item, even received, while ``active`` is true. Out of the window: nothing.

    No ban: not for an item whose bit detects a location (see GatedLocation).

    Attributes:
        item_id: Item to remove.
        active: Whether the window is open this tick.
        clear_bit: Also put the bit back to 0. If False, only the forward is cut,
            so a bit set by the game is kept.
    """

    item_id: int
    active: Callable[[TickContext], bool]
    clear_bit: bool = True


@dataclass(frozen=True)
class TextPatch:
    """Replace ``original`` with ``replacement`` at ``address`` while ``active`` is true.

    Out of the window: nothing, the original is never written back.

    Attributes:
        address: Address of the text in RAM.
        original: Bytes expected in RAM. Anything else is left untouched.
        replacement: Bytes to write, same size as ``original``.
        active: Whether the patch applies this tick.

    Raises:
        ValueError: If ``original`` and ``replacement`` have different sizes.
    """

    address: int
    original: bytes
    replacement: bytes
    active: Callable[[TickContext], bool]

    def __post_init__(self) -> None:
        if len(self.original) != len(self.replacement):
            raise ValueError(
                f"Text sizes differ at {self.address:#x}: {len(self.original)} and {len(self.replacement)}"
            )


@dataclass(frozen=True)
class TrapSpec:
    """Temporary effect of a trap item. Not used by ``plan_tick`` yet.

    Attributes:
        item_id: Trap item.
        duration_s: How long the effect lasts, in seconds.
        apply: Operations starting the effect.
        restore: Operations ending the effect.
        can_start: Whether the trap can start this tick.
    """

    item_id: int
    duration_s: int
    apply: Callable[[TickContext], list[RamOperation]]
    restore: Callable[[TickContext], list[RamOperation]]
    can_start: Callable[[TickContext], bool]


def plan_tick(ctx: TickContext, armed: frozenset[int], traps: TrapState = NO_TRAPS, dt: float = 0.0) -> TickPlan:
    """Build the plan of one tick from the template tables.

    Pure function: it only reads ``ctx``, ``armed`` and the tables. A removal wins over a forced bit.

    Args:
        ctx: Snapshot of the current tick.
        armed: Locations armed at the previous tick.
        traps: Trap state of the previous tick (none by default).
        dt: Seconds elapsed since the previous tick, counted down on the active trap.

    Returns:
        The plan of this tick, with the locations armed for the next one in ``armed``.
    """
    global PREVIOUS_CONTINUE  # noqa: PLW0603

    forced_on, forward_cut, to_clear, banned, new_armed = set(), set(), set(), set(), set()
    raw_ops: list[tuple[int, RamOperation]] = []
    queue = traps.queue + tuple(i for i in ctx.received_order[traps.seen :] if i in TRAPS)
    active = traps.active
    remaining = traps.remaining_s

    for w in FORCE_WINDOWS:  # Betilla already checked
        if w.active(ctx):
            forced_on.add(w.item_id)
        elif w.item_id not in ctx.received and w.location_id not in ctx.missing:
            to_clear.add(w.item_id)  # also true with location_id=None

    for g in GATED_LOCATIONS:  # Betilla, item received
        if g.location_id not in ctx.missing or g.item_id not in ctx.received:
            continue
        if not g.in_zone(ctx):
            banned.add(g.location_id)
            continue
        # MERGE NOTE (Betilla level): from here on, the gate also acts INSIDE Betilla's level
        # (power no longer given, bit cleared, then location armed). The Betilla level handling from
        # the other branch must either replace this block or build on it: both acting on the same
        # power bit would conflict. Removing it without a replacement sends a false check when
        # entering the level with the power already received.
        forward_cut.add(g.item_id)
        if g.location_id in armed or not ctx.location_bits.get(g.location_id, True):
            new_armed.add(g.location_id)  # armed: the bit is no longer touched
        else:
            banned.add(g.location_id)
            to_clear.add(g.item_id)  # cleared only before arming

    for r in REMOVE_WINDOWS:  # removal of an item, even received
        if r.active(ctx):
            forward_cut.add(r.item_id)
            if r.clear_bit:
                to_clear.add(r.item_id)

    # a new operation on every tick
    raw_ops.extend((p.address, ReplaceIfOperation(p.original, p.replacement)) for p in TEXT_PATCHES if p.active(ctx))

    for fo in FREE_OPERATIONS:
        if fo.condition(ctx):
            raw_ops.extend(fo.op(ctx))

    forced_on -= to_clear  # removal wins
    PREVIOUS_CONTINUE = ctx.state["continue_counter"]

    # Traps management
    if active is not None:
        spec = TRAPS[active]
        if spec.can_start(ctx):
            remaining -= dt
        if remaining <= 0:
            raw_ops.extend(spec.restore(ctx))
            active, remaining = None, 0.0

    if active is None and queue and TRAPS[queue[0]].can_start(ctx):
        active = queue[0]
        remaining = TRAPS[queue[0]].duration_s
        queue = queue[1:]

    if active is not None:
        raw_ops.extend(TRAPS[active].apply(ctx))

    return TickPlan(
        frozenset(banned),
        frozenset(forced_on),
        frozenset(forward_cut),
        frozenset(to_clear),
        frozenset(new_armed),
        tuple(raw_ops),
        traps=TrapState(len(ctx.received_order), queue, active, remaining),
    )


class TickTracker:
    """Keep the memory needed between ticks (the armed locations) and build each plan."""

    def __init__(self, clock=time.monotonic) -> None:
        self.armed: frozenset[int] = frozenset()
        self.traps = TrapState()
        self.clock = clock
        self.last_tick = clock()

    def plan(self, ctx: TickContext) -> TickPlan:
        """Build the plan of this tick and remember its armed locations.

        Args:
            ctx: Snapshot of the current tick.

        Returns:
            The plan of this tick.
        """
        now = self.clock()
        dt = min(now - self.last_tick, 1)
        self.last_tick = now
        plan = plan_tick(ctx, self.armed, self.traps, dt)
        self.armed = plan.armed  # updated right away: arming depends on what was read, not on the write
        self.traps = plan.traps
        return plan


# --------Building blocks for callable object---#


def in_level(world: int, level: int) -> Callable[[TickContext], bool]:
    def check(c: TickContext) -> bool:
        return c.state["world_id"] == world and c.state["level_id"] == level

    return check


def in_rect(x_min: int, x_max: int, y_min: int, y_max: int) -> Callable[[TickContext], bool]:
    def check(c: TickContext) -> bool:
        return x_min <= c.state["pos_x"] <= x_max and y_min <= c.state["pos_y"] <= y_max

    return check


def at_pos_x(x: int) -> Callable[[TickContext], bool]:
    def check(c: TickContext) -> bool:
        return x == c.state["pos_x"]

    return check


def not_received(item_id: int) -> Callable[[TickContext], bool]:
    return lambda c: item_id not in c.received


def location_checked(location_id: int) -> Callable[[TickContext], bool]:
    return lambda c: location_id not in c.missing


def option_on(name: str) -> Callable[[TickContext], bool]:
    return lambda c: bool(c.slot_data.get(name, 0))


def received(item_id: int) -> Callable[[TickContext], bool]:
    return lambda c: item_id in c.received


def not_(cond: Callable[[TickContext], bool]) -> Callable[[TickContext], bool]:
    return lambda c: not cond(c)


def all_of(*conds):
    return lambda c: all(cond(c) for cond in conds)


def any_of(*conds):
    return lambda c: any(cond(c) for cond in conds)


# -----Powers conditions
FIST_GIVEN_BY_BETILLA = all_of(
    in_level(1, 3), location_checked(BETILLA_GIFT_1_LOCATION_ID), not_received(TELESCOPIC_FIST_ITEM_ID)
)
FIST_TO_GIVE_TO_SKIP_BETILLA = all_of(
    in_level(1, 2),
    in_rect(0xC51, 0xC63, 0x117, 0x13A),
    not_received(TELESCOPIC_FIST_ITEM_ID),
    location_checked(BETILLA_GIFT_1_LOCATION_ID),
)

HANG_GIVEN_BY_BETILLA = all_of(
    in_level(1, 8), location_checked(BETILLA_GIFT_2_LOCATION_ID), not_received(HANGING_ITEM_ID)
)
HANG_TO_GIVE_TO_SKIP_BETILLA = all_of(
    in_level(1, 7),
    in_rect(0x2500, 0x2555, 0x15, 0x75),
    not_received(HANGING_ITEM_ID),
    location_checked(BETILLA_GIFT_2_LOCATION_ID),
)

GRAPPLING_FIST_GIVEN_BY_BETILLA = all_of(
    in_level(1, 17), location_checked(BETILLA_GIFT_3_LOCATION_ID), not_received(GRAPPLING_FIST_ITEM_ID)
)
GRAPPLING_FIST_TO_GIVE_TO_SKIP_BETILLA = all_of(
    in_level(1, 16), not_received(GRAPPLING_FIST_ITEM_ID), location_checked(BETILLA_GIFT_3_LOCATION_ID)
)

# -----States
SEED_GIVEN = all_of(option_on("magic_seed_as_item"), received(MAGIC_SEED_ITEM_ID))
# --------Zones
SWAMPS_ZONE = in_level(1, 9)
FIST_ZONE = any_of(all_of(in_level(1, 2), in_rect(0xC51, 0xC63, 0x117, 0x13A)), in_level(1, 3))
HANG_ZONE = any_of(all_of(in_level(1, 7), in_rect(0x2500, 0x2555, 0x15, 0x75)), in_level(1, 8))
GRAPPLING_ZONE = any_of(in_level(1, 16), in_level(1, 17))


# World 1
PINK_PLANT_WOOD_CHECKPOINT = all_of(in_level(1, 2), in_rect(0x8CC, 0x906, 0x17A, 0x1D2))
MOSKITO_NEST_CHECKPOINT = all_of(in_level(1, 12), in_rect(0xA04, 0xA3A, 0x159, 0x1C2))
MOSKITO_NEST_CHECKPOINT2 = all_of(in_level(1, 13), in_rect(0x1016, 0x104E, 0x87, 0xF2))

WORLD1_CHECKPOINTS = any_of(PINK_PLANT_WOOD_CHECKPOINT, MOSKITO_NEST_CHECKPOINT, MOSKITO_NEST_CHECKPOINT2)

# World 2
BONGO_HEIGHT_CHECKPOINT = all_of(in_level(2, 3), in_rect(0x192, 0x1C2, 0xE5D, 0xEC2))
BONGO_HEIGHT_CHECKPOINT2 = all_of(in_level(2, 3), in_rect(0x235, 0x263, 0x54B, 0x5B2))
BONGO_HEIGHT_CHECKPOINT3 = all_of(in_level(2, 5), in_rect(0x760, 0x7A2, 0x12, 0x62))
ALEGRO_PRESTO_CHECKPOINT = all_of(in_level(2, 8), in_rect(0x795, 0x7D5, 0x352, 0x3A2))
ALEGRO_PRESTO_CHECKPOINT2 = all_of(in_level(2, 9), in_rect(0xD32, 0xD58, 0x268, 0x2C2))
ALEGRO_PRESTO_CHECKPOINT3 = all_of(in_level(2, 10), in_rect(0x6A8, 0x6DE, 0x3AA, 0x402))
SAX_HULLABALOO_CHECKPOINT3 = all_of(in_level(2, 14), in_rect(0x86, 0xB6, 0x1AA, 0x202))

WORLD2_CHECKPOINTS = any_of(
    BONGO_HEIGHT_CHECKPOINT,
    BONGO_HEIGHT_CHECKPOINT2,
    BONGO_HEIGHT_CHECKPOINT3,
    ALEGRO_PRESTO_CHECKPOINT,
    ALEGRO_PRESTO_CHECKPOINT2,
    ALEGRO_PRESTO_CHECKPOINT3,
    SAX_HULLABALOO_CHECKPOINT3,
)

# world 3
TWILIGHT_GULCH_CHECKPOINT = all_of(in_level(3, 4), in_rect(0x865, 0x899, 0x195, 0x1E2))
TWILIGHT_GULCH_CHECKPOINT2 = all_of(in_level(3, 5), in_rect(0x272, 0x2AC, 0x4CF, 0x522))
STONE_PEAK_CHECKPOINT = all_of(in_level(3, 6), in_rect(0xBFA, 0xC30, 0xB9, 0x102))
STONE_PEAK_CHECKPOINT2 = all_of(in_level(3, 6), in_rect(0x143F, 0x1465, 0x15E, 0x1A2))
STONE_PEAK_CHECKPOINT3 = all_of(in_level(3, 9), in_rect(0x12DC, 0x1308, 0x149, 0x192))

WORLD3_CHECKPOINTS = any_of(
    TWILIGHT_GULCH_CHECKPOINT,
    TWILIGHT_GULCH_CHECKPOINT2,
    STONE_PEAK_CHECKPOINT,
    STONE_PEAK_CHECKPOINT2,
    STONE_PEAK_CHECKPOINT3,
)

# world 4
ERASER_PLAINS_CHECKPOINT = all_of(in_level(4, 1), in_rect(0xA1D, 0xA4B, 0x109, 0x152))
PENCIL_PENTATHLON_CHECKPOINT = all_of(in_level(4, 5), in_rect(0x8A1, 0x8CF, 0x14A, 0x1A2))
PENCIL_PENTATHLON_CHECKPOINT2 = all_of(in_level(4, 6), in_rect(0xA66, 0xA94, 0xFA, 0x152))
PENCIL_PENTATHLON_CHECKPOINT3 = all_of(in_level(4, 6), in_rect(0xF04, 0xF3C, 0x14B, 0x192))
PENCIL_PENTATHLON_CHECKPOINT4 = all_of(in_level(4, 7), in_rect(0x4DD, 0x501, 0x142, 0x192))
MAMA_CRATER_CHECKPOINT = all_of(in_level(4, 8), in_rect(0xD30, 0xD66, 0x339, 0x382))
MAMA_CRATER_CHECKPOINT2 = all_of(in_level(4, 9), in_rect(0x61E, 0x64C, 0x58, 0x92))
MAMA_CRATER_CHECKPOINT3 = all_of(in_level(4, 10), in_rect(0x9E, 0xCE, 0x16, 0x62))
MAMA_CRATER_CHECKPOINT4 = all_of(in_level(4, 10), in_rect(0x45D, 0x491, 0x1B1, 0x1F2))

WORLD4_CHECKPOINTS = any_of(
    ERASER_PLAINS_CHECKPOINT,
    PENCIL_PENTATHLON_CHECKPOINT,
    PENCIL_PENTATHLON_CHECKPOINT2,
    PENCIL_PENTATHLON_CHECKPOINT3,
    PENCIL_PENTATHLON_CHECKPOINT4,
    MAMA_CRATER_CHECKPOINT,
    MAMA_CRATER_CHECKPOINT2,
    MAMA_CRATER_CHECKPOINT3,
    MAMA_CRATER_CHECKPOINT4,
)

# world 5
CRYSTAL_PALACE_CHECKPOINT = all_of(in_level(5, 1), in_rect(0x858, 0x88E, 0x19, 0x62))
CRYSTAL_PALACE_CHECKPOINT2 = all_of(in_level(5, 2), in_rect(0xAE7, 0xB0F, 0x1CD, 0x212))
EAT_AT_JOE_CHECKPOINT = all_of(in_level(5, 5), in_rect(0x336, 0x36E, 0x31D, 0x362))
SKOP_CHECKPOINT = all_of(in_level(5, 9), in_rect(0xBAA, 0x38A, 0x36C, 0x3B2))

WORLD5_CHECKPOINTS = any_of(
    CRYSTAL_PALACE_CHECKPOINT, CRYSTAL_PALACE_CHECKPOINT2, EAT_AT_JOE_CHECKPOINT, SKOP_CHECKPOINT
)

# world 6
DARK_DARE_CHECKPOINT = all_of(in_level(6, 3), in_rect(0x660, 0x697, 0x25, 0x100))
DARK_DARE_CHECKPOINT2 = all_of(in_level(6, 3), in_rect(0xB1E, 0xB50, 0x245, 0x292))
DARK_DARE_CHECKPOINT3 = all_of(in_level(6, 3), in_rect(0x12F4, 0x132C, 0x272, 0x2C2))

WORLD6_CHECKPOINTS = any_of(DARK_DARE_CHECKPOINT, DARK_DARE_CHECKPOINT2, DARK_DARE_CHECKPOINT3)

CHECKPOINTS = any_of(
    WORLD1_CHECKPOINTS,
    WORLD2_CHECKPOINTS,
    WORLD3_CHECKPOINTS,
    WORLD4_CHECKPOINTS,
    WORLD5_CHECKPOINTS,
    WORLD6_CHECKPOINTS,
)


# ------SCENES
LOST_SEED_SCENE = all_of(SWAMPS_ZONE, not_received(MAGIC_SEED_ITEM_ID), option_on("magic_seed_as_item"))
NO_SEED_OUTSIDE_SWAMPS = all_of(option_on("magic_seed_as_item"), received(MAGIC_SEED_ITEM_ID), not_(SWAMPS_ZONE))
SEED_TEXT_RESTORE = all_of(SWAMPS_ZONE, SEED_GIVEN)
NO_FIST_IF_NOT_RECEIVED = all_of(not_(in_level(1, 3)))
FORCE_WINDOWS: tuple[ForceWindow, ...] = (
    ForceWindow(  # Force the fist power to be granted to the player
        TELESCOPIC_FIST_ITEM_ID, any_of(FIST_GIVEN_BY_BETILLA, FIST_TO_GIVE_TO_SKIP_BETILLA), BETILLA_GIFT_1_LOCATION_ID
    ),
    ForceWindow(  # Force the hang power to be granted to the player
        HANGING_ITEM_ID, any_of(HANG_GIVEN_BY_BETILLA, HANG_TO_GIVE_TO_SKIP_BETILLA), BETILLA_GIFT_2_LOCATION_ID
    ),
    ForceWindow(  # Force the grappling fist power to be granted to the player
        GRAPPLING_FIST_ITEM_ID,
        any_of(GRAPPLING_FIST_GIVEN_BY_BETILLA, GRAPPLING_FIST_TO_GIVE_TO_SKIP_BETILLA),
        BETILLA_GIFT_3_LOCATION_ID,
    ),
)
GATED_LOCATIONS: tuple[GatedLocation, ...] = (
    GatedLocation(BETILLA_GIFT_1_LOCATION_ID, TELESCOPIC_FIST_ITEM_ID, FIST_ZONE),
    GatedLocation(BETILLA_GIFT_2_LOCATION_ID, HANGING_ITEM_ID, HANG_ZONE),
    GatedLocation(BETILLA_GIFT_3_LOCATION_ID, GRAPPLING_FIST_ITEM_ID, GRAPPLING_ZONE),
    # A check si ce sont les bonnes
)
REMOVE_WINDOWS: tuple[RemoveWindow, ...] = (
    # MAGIC_SEED
    RemoveWindow(MAGIC_SEED_ITEM_ID, LOST_SEED_SCENE),  # not received, in 1-9
    RemoveWindow(MAGIC_SEED_ITEM_ID, NO_SEED_OUTSIDE_SWAMPS),  # received, outside 1-9
    # Tarayzan gives the seed back: no forward, and the bit set by the game is not cleared
    RemoveWindow(MAGIC_SEED_ITEM_ID, SEED_GIVEN, clear_bit=False),
)
TEXT_PATCHES: tuple[TextPatch, ...] = (
    # MAGIC_SEED
    TextPatch(
        address=MAGIC_SEED_TEXT_1_ADDRESS,
        original=MAGIC_SEED_TEXT_1_ORIGINAL,
        replacement=MAGIC_SEED_TEXT_1_REPLACEMENT,
        active=LOST_SEED_SCENE,
    ),
    TextPatch(
        address=MAGIC_SEED_TEXT_2_ADDRESS,
        original=MAGIC_SEED_TEXT_2_ORIGINAL,
        replacement=MAGIC_SEED_TEXT_2_REPLACEMENT,
        active=LOST_SEED_SCENE,
    ),
    # Seed received: put the original text back if the "lost" text is still in RAM
    TextPatch(
        address=MAGIC_SEED_TEXT_1_ADDRESS,
        original=MAGIC_SEED_TEXT_1_REPLACEMENT,
        replacement=MAGIC_SEED_TEXT_1_ORIGINAL,
        active=SEED_TEXT_RESTORE,
    ),
    TextPatch(
        address=MAGIC_SEED_TEXT_2_ADDRESS,
        original=MAGIC_SEED_TEXT_2_REPLACEMENT,
        replacement=MAGIC_SEED_TEXT_2_ORIGINAL,
        active=SEED_TEXT_RESTORE,
    ),
)
TRAPS: dict[int, TrapSpec] = {
    10001: TrapSpec(
        item_id=REVERSED_CONTROL_ITEM_ID,
        duration_s=30.0,
        apply=lambda c: [(0x1F43D1, MaskOperation(1, set_mask=0x20))],
        restore=lambda c: [(0x1F43D1, MaskOperation(1, clear_mask=0x20))],
        can_start=lambda c: True,
    ),
    10002: TrapSpec(
        item_id=FORCED_RUN_ITEM_ID,
        duration_s=5.0,
        apply=lambda c: [(0x1F43D1, MaskOperation(1, set_mask=0x10))],
        restore=lambda c: [(0x1F43D1, MaskOperation(1, clear_mask=0x10))],
        can_start=lambda c: True,
    ),
}
FREE_OPERATIONS: tuple[FreeOperation, ...] = (
    FreeOperation(  # Number of starting life option
        condition=lambda c: (
            c.slot_data["number_of_starting_life"] != 3
            and c.state["starting_life_option_applied"] != 1
            and c.state["life_counter"] == 3
        ),
        op=lambda c: [
            (0x1E4D50, SetOperation(1, c.slot_data["number_of_starting_life"])),
            (0x1F9B20, SetOperation(1, 1)),
        ],
    ),
    FreeOperation(  # Reapply the base number of life if a continue has been used
        condition=lambda c: c.state["continue_counter"] < PREVIOUS_CONTINUE,
        op=lambda c: [(0x1F9B20, SetOperation(1, 0))],
    ),
    FreeOperation(  # Number of continue option
        condition=lambda c: c.slot_data["number_of_continue"] != 5 and c.state["number_continue_option_applied"] != 1,
        op=lambda c: [(0x1E5A10, SetOperation(1, c.slot_data["number_of_continue"])), (0x1F9B21, SetOperation(1, 1))],
    ),
    FreeOperation(  # Number of tings to get a new life option
        condition=lambda c: (
            c.slot_data["number_of_tings_to_get_a_new_life"] != 100
            and c.state["tings_counter"] >= c.slot_data["number_of_tings_to_get_a_new_life"]
        ),
        op=lambda c: [
            (0x1E4D50, SetOperation(1, c.state["life_counter"] + 1)),
            (0x1E4D56, SetOperation(1, c.state["tings_counter"] - c.slot_data["number_of_tings_to_get_a_new_life"])),
        ],
    ),
    FreeOperation(  # Apply death link
        condition=lambda c: (
            c.death_link_pending
            and c.state["is_death_link_applied"] == 0
            and c.state["is_taking_sign"] == 0
            and not CHECKPOINTS(c)
        ),
        op=lambda c: [(0x1E5420, SetOperation(1, 3)), (0x1F9B22, SetOperation(1, 1))],
    ),
    FreeOperation(  # Received death over: Rayman is alive again, the next DeathLink can be applied
        condition=lambda c: (
            c.state["is_death_link_applied"] == 1 and c.state["rayman_mode"] != 3 and c.state["is_rayman_drowning"] == 0
        ),
        op=lambda c: [(0x1F9B22, SetOperation(1, 0))],
    ),
    FreeOperation(  # removed run after trap
        condition=lambda c: 1005 not in c.received, op=lambda c: [(0x1F43D1, MaskOperation(1, clear_mask=0x1))]
    ),
)
