from dataclasses import dataclass
from .ram_operation import RamOperation, ReplaceIfOperation
from collections.abc import Callable

@dataclass(frozen=True)
class TickContext:
    state: dict[str, int]            # STATE_READS (world, level, x, y, menu, ...)
    received: frozenset[int]         # ids des items reçus
    missing: frozenset[int]          # locations pas encore checkées
    location_bits: dict[int, bool]   # bit lu de chaque location manquante (1er read)
    slot_data: dict

@dataclass(frozen=True)
class TickPlan:
    banned_locations: frozenset[int]   # ne partent pas au serveur ce tick
    forced_on: frozenset[int]          # items posés à 1 sans être reçus
    forward_cut: frozenset[int]        # items reçus, mais pas redonnés ce tick
    to_clear: frozenset[int]           # items dont le bit est remis à 0
    armed: frozenset[int]              # locations armées, reprises au tick suivant
    raw_ops: tuple[tuple[int, RamOperation], ...] = ()  # (adresse, opération) sans item ni location

@dataclass(frozen=True)
class ForceWindow:
    item_id: int
    active: Callable[[TickContext], bool]
    location_id: int | None = None   # location liée à l'item (None pour la seed)

@dataclass(frozen=True)
class GatedLocation:
    location_id: int
    item_id: int
    in_zone: Callable[[TickContext], bool]

@dataclass(frozen=True)
class RemoveWindow:
    """Retire un item, même reçu, tant que ``active`` est vrai. Hors fenêtre : rien.

    Pas de ban : à ne pas utiliser pour un item dont le bit détecte une location (voir GatedLocation).
    """
    item_id: int
    active: Callable[[TickContext], bool]

@dataclass(frozen=True)
class TextPatch:
    """Remplace ``original`` par ``replacement`` à ``address`` tant que ``active`` est vrai.

    Hors fenêtre : rien, l'original n'est jamais réécrit.
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
    item_id: int
    duration_s: float
    apply: Callable[[TickContext], list[RamOperation]]
    restore: Callable[[TickContext], list[RamOperation]]
    can_start: Callable[[TickContext], bool]


FORCE_WINDOWS: tuple[ForceWindow, ...] = (
    ForceWindow(item_id=2001,
                active=
                ,location_id=None,)
)
GATED_LOCATIONS: tuple[GatedLocation, ...] = ()
TRAPS: dict[int, TrapSpec] = {}

def plan_tick(ctx: TickContext, armed: frozenset[int]) -> TickPlan:
    forced_on, forward_cut, to_clear, banned, new_armed = set(), set(), set(), set(), set()
    raw_ops: list[tuple[int, RamOperation]] = []

    for w in FORCE_WINDOWS:           # seed, Betilla déjà faite
        if w.active(ctx):
            forced_on.add(w.item_id)
        elif w.item_id not in ctx.received and w.location_id not in ctx.missing:
            to_clear.add(w.item_id)    # location_id=None pour la seed

    for g in GATED_LOCATIONS:          # Betilla, item reçu
        if g.location_id not in ctx.missing or g.item_id not in ctx.received:
            continue
        if not g.in_zone(ctx):
            banned.add(g.location_id)
            continue
        forward_cut.add(g.item_id)
        if g.location_id in armed or not ctx.location_bits.get(g.location_id, True):
            new_armed.add(g.location_id)       # armée : on ne touche plus au bit
        else:
            banned.add(g.location_id)
            to_clear.add(g.item_id)            # efface seulement avant l'armement

    for r in REMOVE_WINDOWS:           # retrait d'un item, même reçu
        if r.active(ctx):
            forward_cut.add(r.item_id)
            to_clear.add(r.item_id)

    for p in TEXT_PATCHES:             # une nouvelle opération à chaque tick
        if p.active(ctx):
            raw_ops.append((p.address, ReplaceIfOperation(p.original, p.replacement)))

    forced_on -= to_clear              # le retrait l'emporte

    return TickPlan(frozenset(banned), frozenset(forced_on), frozenset(forward_cut),
                    frozenset(to_clear), frozenset(new_armed), tuple(raw_ops))

class TickTracker:
    def __init__(self) -> None:
        self.armed: frozenset[int] = frozenset()

    def plan(self, ctx: TickContext) -> TickPlan:
        plan = plan_tick(ctx, self.armed)
        self.armed = plan.armed    # mis à jour tout de suite, pas de commit
        return plan


#--------Building blocks for callable object---#
def on_world_map_level():
    pass

def in_level(world: int, level: int) -> Callable[[TickContext], bool]:
    def check(c: TickContext) -> bool:
        return c.state["world_id"] == world and c.state["level_id"] == level
    return check

def in_rect(x_min: int, x_max: int, y_min: int, y_max: int) -> Callable[[TickContext], bool]:
    def check(c: TickContext) -> bool:
        return (x_min <= c.state["pos_x"] <= x_max
                and y_min <= c.state["pos_y"] <= y_max)
    return check

def all_of(*conds): return lambda c: all(cond(c) for cond in conds)
def any_of(*conds): return lambda c: any(cond(c) for cond in conds)

REMOVE_WINDOWS: tuple[RemoveWindow, ...] = ()
TEXT_PATCHES: tuple[TextPatch, ...] = ()

#zones

