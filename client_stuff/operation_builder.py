from collections.abc import Collection
import logging

from ..items import ITEM_ID_TABLE, ItemData
from ..locations import LOCATION_ID_TABLE
from .effect_strategy import STRATEGIES, RamOps
from .ram_operation import RamOperation, MaskOperation, SetOperation
from .ram_map import ITEM_COUNTER_ADDRESS, ITEM_COUNTER_SIZE, RESTORED_ITEM_IDS
from ..utils import Effect
logger = logging.getLogger("OperationBuilder")

def _merge_into(ops: dict[int, RamOperation], new_ops: RamOps) -> None:
    """Merge ``new_ops`` into ``ops`` (in place), one operation per address.

    On conflict (see ``RamOperation.merge``), the first operation is kept and an error is logged.
    """
    for address, op in new_ops:
        target_op = ops.get(address)
        if target_op is None:
            ops[address] = op
        else:
            try:
                target_op.merge(op)
            except (TypeError, ValueError) as e:
                logger.error(f"Merging of {op} into {target_op} at {address:#x} failed, keeping the first one: {e}")


def _add_item_operations(ops: dict[int, RamOperation],
                         items_received: list[int],
                         counter_state: int = 0,
                         to_ban: Collection[int] = frozenset(),
                         delivered_consumables: int = 0) -> None:
    """Merge the forward operations of the received items into ``ops`` (in place).

    Args:
        ops: Operations being built, one per address.
        items_received: Ids of all received items, in reception order.
        counter_state: Number of items already applied. Items of an ``apply_once``
            strategy with an index below it are skipped.
        delivered_consumables: Number of items already given, kept on the server. ``apply_once`` items
            with an index below it are skipped even if ``counter_state`` went back to 0, except
            ``RESTORED_ITEM_IDS``.
    """
    for index, item_id in enumerate(items_received):
        item = ITEM_ID_TABLE.get(item_id)
        if item is None:
            logger.warning(f"Unknown id in ITEM_ID_TABLE: {item_id}")
            continue
        strategy = STRATEGIES[item.effect]
        if item_id in to_ban and not strategy.apply_once:
                    continue
        applied = counter_state if item_id in RESTORED_ITEM_IDS else max(counter_state, delivered_consumables)
        if strategy.apply_once and index < applied:
            continue
        _merge_into(ops, strategy.forward(item))


def _add_counter_operation(ops: dict[int, RamOperation], items_received: list[int], counter_state: int) -> None:
    """Write the number of applied items to the game's RAM, in the same write as the items. Never goes backwards."""
    if len(items_received) > counter_state:
        _merge_into(ops, [(ITEM_COUNTER_ADDRESS, SetOperation(size=ITEM_COUNTER_SIZE, value=len(items_received)))])


def _add_location_reverse_operations(ops: dict[int, RamOperation], to_reverse: set[int]) -> None:
    """Merge the reverse of each location's vanilla item into ``ops`` (in place).

    Cancels what the game gave when the location was checked (e.g. -1 life for a life status),
    so the player only keeps what Archipelago sends. Locations without vanilla item are ignored.

    Args:
        ops: Operations being built, one per address.
        to_reverse: Ids of the locations to reverse. Must only contain locations detected in game
            and not yet checked on the server (built by the client from ``missing_locations``),
            each one passed once.
    """
    for loc_id in to_reverse:
        loc = LOCATION_ID_TABLE.get(loc_id)
        if loc is None:
            logger.warning(f"Unknown id in LOCATION_ID_TABLE: {loc_id}")
            continue
        item_id = loc.vanilla_item
        if item_id is None:
            continue
        item = ITEM_ID_TABLE.get(item_id)
        if item is None:
            logger.warning(f"Unknown id in ITEM_ID_TABLE: {item_id}")
            continue
        strategy = STRATEGIES[item.effect]
        _merge_into(ops, strategy.reverse(item))


def _add_location_resync_operations(ops: dict[int, RamOperation], checked_ids: set[int]) -> None:
    """Merge into ``ops`` (in place) the operations setting the flag of every checked location.

    Keeps the game in sync with the server: a location checked on the server stays collected
    in game (e.g. after a restart without saving). Idempotent, safe to run on every tick.

    Args:
        ops: Operations being built, one per address.
        checked_ids: Ids of the locations already checked on the server (``ctx.checked_locations``).
    """
    for loc_id in checked_ids:
        loc = LOCATION_ID_TABLE.get(loc_id)
        if loc is None:
            continue
        vanilla = ITEM_ID_TABLE.get(loc.vanilla_item) if loc.vanilla_item is not None else None
        if vanilla is not None and vanilla.effect is Effect.BIT:
            continue   # Betilla: the flag IS the power bit, setting it would give the power
        _merge_into(ops, [(loc.address, MaskOperation(size=loc.size.value, set_mask=loc.mask))])


def _event_bit_item(item_id: int, reason: str) -> ItemData | None:
    item = ITEM_ID_TABLE.get(item_id)
    if item is None:
        logger.warning(f"Unknown id in ITEM_ID_TABLE: {item_id}")
        return None
    if item.effect is not Effect.BIT:
        logger.warning(f"Forbidden id for BIT only: {item_id}")
        return None
    return item

def _add_event_operations(ops, to_apply: Collection[int], to_remove: Collection[int]) -> None:
    """Bits forced by the tick plan, independently of items_received. BIT only."""
    for item_id in to_apply:
        if item := _event_bit_item(item_id, "apply"):
            _merge_into(ops, STRATEGIES[item.effect].forward(item))
    for item_id in to_remove:
        if item := _event_bit_item(item_id, "removal"):
            _merge_into(ops, STRATEGIES[item.effect].reverse(item))

def build_ram_operations(items_received: list[int],
                         counter_state: int,
                         checked_ids: set[int],
                         to_reverse: set[int],
                         to_ban : Collection[int] = frozenset(),
                         to_apply : Collection[int] = frozenset(),
                         to_remove : Collection[int] = frozenset(),
                         raw_ops : Collection[tuple[int, RamOperation]] = (),
                         delivered_consumables: int = 0) -> dict[int, RamOperation]:
    """Build every RAM operation of a tick, merged by address.

    Args:
        items_received: Ids of all received items, in reception order.
        counter_state: Number of items already applied, read in the game's RAM at ``ITEM_COUNTER_ADDRESS``
            (0x1F9C52). See ``_add_item_operations``; rewritten by ``_add_counter_operation``.
        checked_ids: Ids of the locations already checked on the server.
        to_reverse: Ids of the locations whose vanilla item must be reversed.
        raw_ops: Ready-made (address, operation) pairs from the tick plan, not tied to an item or a location.
        delivered_consumables: Number of items whose consumables were already given (see ``_add_item_operations``).

    Returns:
        One operation per address, ready to be read, applied and written by the client.
    """
    ops: dict[int, RamOperation] = {}
    _add_item_operations(ops, items_received, counter_state, to_ban, delivered_consumables)
    _add_counter_operation(ops, items_received, counter_state)
    _add_event_operations(ops, to_apply, to_remove)
    _merge_into(ops, raw_ops)
    _add_location_resync_operations(ops, checked_ids)
    _add_location_reverse_operations(ops, to_reverse)

    return ops


