import time
from dataclasses import dataclass
from .ram_operation import RamOperation, ReplaceIfOperation, MaskOperation
from collections.abc import Callable
from .ram_map import MAGIC_SEED_ITEM_ID, FIST_ITEM_ID, HANG_ITEM_ID, GRAPPLING_FIST_ITEM_ID, HELICOPTER_ITEM_ID
from .ram_map import BETILLA_GIFT_1_LOCATION_ID, BETILLA_GIFT_2_LOCATION_ID, BETILLA_GIFT_3_LOCATION_ID
from .ram_map import REVERSED_CONTROL_ITEM_ID, FORCED_RUN_ITEM_ID
from .ram_map import MAGIC_SEED_TEXT_1_ADDRESS, MAGIC_SEED_TEXT_1_ORIGINAL, MAGIC_SEED_TEXT_1_REPLACEMENT
from .ram_map import MAGIC_SEED_TEXT_2_ADDRESS, MAGIC_SEED_TEXT_2_ORIGINAL, MAGIC_SEED_TEXT_2_REPLACEMENT

@dataclass(frozen=True)
class TrapState:
    seen: int = 0
    queue: tuple[int, ...] = ()
    active: int | None = None
    remaining_s: float = 0.0

@dataclass(frozen=True)
class TickContext:
    """Snapshot of the game and the server for one tick, taken from the first read."""
    state: dict[str, int]            # STATE_READS (world, level, x, y, menu, ...)
    received: frozenset[int]         # ids of the received items
    missing: frozenset[int]          # locations not checked yet
    location_bits: dict[int, bool]   # bit read for each missing location (first read)
    slot_data: dict
    received_order: tuple[int, ...] = ()

@dataclass(frozen=True)
class TickPlan:
    """What the special events decided for one tick, applied by the client and the builder."""
    banned_locations: frozenset[int]   # not sent to the server this tick
    forced_on: frozenset[int]          # items whose bit is set without being received
    forward_cut: frozenset[int]        # received items not given again this tick
    to_clear: frozenset[int]           # items whose bit is put back to 0
    armed: frozenset[int]              # armed locations, kept for the next tick
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
    location_id: int | None = None   # location tied to the item (None for an item without location)

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
            raise ValueError(f"Text sizes differ at {self.address:#x}: "
                             f"{len(self.original)} and {len(self.replacement)}")

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

def plan_tick(ctx: TickContext, armed: frozenset[int], traps: TrapState, dt: float) -> TickPlan:
    """Build the plan of one tick from the template tables.

    Pure function: it only reads ``ctx``, ``armed`` and the tables. A removal wins over a forced bit.

    Args:
        ctx: Snapshot of the current tick.
        armed: Locations armed at the previous tick.

    Returns:
        The plan of this tick, with the locations armed for the next one in ``armed``.
    """
    forced_on, forward_cut, to_clear, banned, new_armed = set(), set(), set(), set(), set()
    raw_ops: list[tuple[int, RamOperation]] = []
    queue = traps.queue + tuple(i for i in ctx.received_order[traps.seen:] if i in TRAPS)
    active = traps.active
    remaining = traps.remaining_s

    for w in FORCE_WINDOWS:           # Betilla already checked
        if w.active(ctx):
            forced_on.add(w.item_id)
        elif w.item_id not in ctx.received and w.location_id not in ctx.missing:
            to_clear.add(w.item_id)    # also true with location_id=None

    for g in GATED_LOCATIONS:          # Betilla, item received
        if g.location_id not in ctx.missing or g.item_id not in ctx.received:
            continue
        if not g.in_zone(ctx):
            banned.add(g.location_id)
            continue
        forward_cut.add(g.item_id)
        if g.location_id in armed or not ctx.location_bits.get(g.location_id, True):
            new_armed.add(g.location_id)       # armed: the bit is no longer touched
        else:
            banned.add(g.location_id)
            to_clear.add(g.item_id)            # cleared only before arming

    for r in REMOVE_WINDOWS:           # removal of an item, even received
        if r.active(ctx):
            forward_cut.add(r.item_id)
            if r.clear_bit:
                to_clear.add(r.item_id)

    for p in TEXT_PATCHES:             # a new operation on     every tick
        if p.active(ctx):
            raw_ops.append((p.address, ReplaceIfOperation(p.original, p.replacement)))

    forced_on -= to_clear              # removal wins

    # Traps management
    print("trap management")
    if active is not None:
        print("trap management")
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
        print("oui c'est bon")
        raw_ops.extend(TRAPS[active].apply(ctx))

    return TickPlan(frozenset(banned), frozenset(forced_on), frozenset(forward_cut),
                    frozenset(to_clear), frozenset(new_armed), tuple(raw_ops),
                    traps=TrapState(len(ctx.received_order), queue, active, remaining))

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
        self.armed = plan.armed    # updated right away: arming depends on what was read, not on the write
        self.traps = plan.traps
        return plan


#--------Building blocks for callable object---#

def in_level(world: int, level: int) -> Callable[[TickContext], bool]:
    def check(c: TickContext) -> bool:
        return c.state["world_id"] == world and c.state["level_id"] == level
    return check

def in_rect(x_min: int, x_max: int, y_min: int, y_max: int) -> Callable[[TickContext], bool]:
    def check(c: TickContext) -> bool:
        return (x_min <= c.state["pos_x"] <= x_max
                and y_min <= c.state["pos_y"] <= y_max)
    return check

def at_pos_x(x:int) -> Callable[[TickContext],bool]:
    def check(c:TickContext) -> bool:
        return (x == c.state["pos_x"])
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

def all_of(*conds): return lambda c: all(cond(c) for cond in conds)
def any_of(*conds): return lambda c: any(cond(c) for cond in conds)



#-----Powers conditions
FIST_GIVEN_BY_BETILLA = all_of(in_level(1,3), location_checked(BETILLA_GIFT_1_LOCATION_ID), not_received(FIST_ITEM_ID))
FIST_TO_GIVE_TO_SKIP_BETILLA = all_of(in_level(1, 2), in_rect(0xC51, 0xC63, 0x117, 0x13A), not_received(FIST_ITEM_ID), location_checked(BETILLA_GIFT_1_LOCATION_ID))

HANG_GIVEN_BY_BETILLA = all_of(in_level(1,8), location_checked(BETILLA_GIFT_2_LOCATION_ID), not_received(HANG_ITEM_ID))
HANG_TO_GIVE_TO_SKIP_BETILLA = all_of(in_level(1,7), in_rect(0x2518, 0x2548, 0x2D, 0x45), not_received(HANG_ITEM_ID), location_checked(BETILLA_GIFT_2_LOCATION_ID))

GRAPPLING_FIST_GIVEN_BY_BETILLA = all_of(in_level(1,17), location_checked(BETILLA_GIFT_3_LOCATION_ID), not_received(GRAPPLING_FIST_ITEM_ID))
GRAPPLING_FIST_TO_GIVE_TO_SKIP_BETILLA = all_of(in_level(1, 16), not_received(GRAPPLING_FIST_ITEM_ID), location_checked(BETILLA_GIFT_3_LOCATION_ID))

#-----States
SEED_GIVEN = all_of(option_on("magic_seed_as_item"), received(MAGIC_SEED_ITEM_ID))
#--------Zones
SWAMPS_ZONE = in_level(1,9)
FIST_ZONE = any_of(all_of(in_level(1, 2), in_rect(0xC51, 0xC63, 0x117, 0x13A)), in_level(1, 3))
HANG_ZONE = any_of(all_of(in_level(1, 7), in_rect(0x2518, 0x2548, 0x2D, 0x45)), in_level(1, 8))
GRAPPLING_ZONE = any_of(in_level(1, 16), in_level(1, 17))

#------SCENES
LOST_SEED_SCENE = all_of(SWAMPS_ZONE,not_received(MAGIC_SEED_ITEM_ID),option_on("magic_seed_as_item"))
NO_SEED_OUTSIDE_SWAMPS = all_of(option_on("magic_seed_as_item"),
                             received(MAGIC_SEED_ITEM_ID),
                             not_(SWAMPS_ZONE))
SEED_TEXT_RESTORE = all_of(SWAMPS_ZONE, SEED_GIVEN)
NO_FIST_IF_NOT_RECEIVED = all_of(not_(in_level(1,3)))



#-------collections of template data
FORCE_WINDOWS: tuple[ForceWindow, ...] = (
    ForceWindow( # Force the fist power to be granted to the player
        FIST_ITEM_ID,
        any_of(FIST_GIVEN_BY_BETILLA, FIST_TO_GIVE_TO_SKIP_BETILLA),
        BETILLA_GIFT_1_LOCATION_ID
    ),
    ForceWindow( # Force the hang power to be granted to the player
        HANG_ITEM_ID,
        any_of(HANG_GIVEN_BY_BETILLA, HANG_TO_GIVE_TO_SKIP_BETILLA),
        BETILLA_GIFT_2_LOCATION_ID
    ),
    ForceWindow( # Force the grappling fist power to be granted to the player
        GRAPPLING_FIST_ITEM_ID,
        any_of(GRAPPLING_FIST_GIVEN_BY_BETILLA, GRAPPLING_FIST_TO_GIVE_TO_SKIP_BETILLA),
        BETILLA_GIFT_3_LOCATION_ID
    ),
)
GATED_LOCATIONS: tuple[GatedLocation, ...] = (
    GatedLocation(2001, 1001, FIST_ZONE),
    GatedLocation(2002, 1002, HANG_ZONE),
    GatedLocation(2003, 1003, GRAPPLING_ZONE),

)
REMOVE_WINDOWS: tuple[RemoveWindow, ...] = (
    #MAGIC_SEED
    RemoveWindow(MAGIC_SEED_ITEM_ID, LOST_SEED_SCENE),                               # not received, in 1-9
    RemoveWindow(MAGIC_SEED_ITEM_ID, NO_SEED_OUTSIDE_SWAMPS),                        # received, outside 1-9
    # Tarayzan gives the seed back: no forward, and the bit set by the game is not cleared
    RemoveWindow(MAGIC_SEED_ITEM_ID, SEED_GIVEN, clear_bit=False),
)
TEXT_PATCHES: tuple[TextPatch, ...] = (
    #MAGIC_SEED
    TextPatch(address=MAGIC_SEED_TEXT_1_ADDRESS,original=MAGIC_SEED_TEXT_1_ORIGINAL,
              replacement=MAGIC_SEED_TEXT_1_REPLACEMENT,active=LOST_SEED_SCENE),
    TextPatch(address=MAGIC_SEED_TEXT_2_ADDRESS,original=MAGIC_SEED_TEXT_2_ORIGINAL,
                  replacement=MAGIC_SEED_TEXT_2_REPLACEMENT,active=LOST_SEED_SCENE),
    # Seed received: put the original text back if the "lost" text is still in RAM
    TextPatch(address=MAGIC_SEED_TEXT_1_ADDRESS,original=MAGIC_SEED_TEXT_1_REPLACEMENT,
              replacement=MAGIC_SEED_TEXT_1_ORIGINAL,active=SEED_TEXT_RESTORE),
    TextPatch(address=MAGIC_SEED_TEXT_2_ADDRESS,original=MAGIC_SEED_TEXT_2_REPLACEMENT,
              replacement=MAGIC_SEED_TEXT_2_ORIGINAL,active=SEED_TEXT_RESTORE),
)
TRAPS: dict[int, TrapSpec] = {
    10001 : TrapSpec(
        item_id=REVERSED_CONTROL_ITEM_ID,
        duration_s=30.0,
        apply=lambda c: [(0x1f43d1, MaskOperation(1, set_mask=0x20))],
        restore=lambda c: [(0x1f43d1, MaskOperation(1, clear_mask=0x20))],
        can_start=lambda c: True
    ),
    10002: TrapSpec(
        item_id=FORCED_RUN_ITEM_ID,
        duration_s=5.0,
        apply=lambda c: [(0x1f43d1, MaskOperation(1, set_mask=0x10))],
        restore=lambda c: [(0x1f43d1, MaskOperation(1, clear_mask=0x10))],
        can_start=lambda c: True
    ),
}
