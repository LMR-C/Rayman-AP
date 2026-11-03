import logging

from ..items import ITEM_ID_TABLE
from ..locations import LOCATION_ID_TABLE
from .effect_strategy import STRATEGIES, RamOps
from .ram_operation import RamOperation
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


def _add_item_operations(ops: dict[int, RamOperation], items_received: list[int], counter_state: int = 0) -> None:
    """Merge the forward operations of the received items into ``ops`` (in place).

    Args:
        ops: Operations being built, one per address.
        items_received: Ids of all received items, in reception order.
        counter_state: Number of items already applied. Items of an ``apply_once``
            strategy with an index below it are skipped.
    """
    for index, item_id in enumerate(items_received):
        item = ITEM_ID_TABLE.get(item_id)
        if item is None:
            logger.warning(f"Unknown id in ITEM_ID_TABLE: {item_id}")
            continue
        strategy = STRATEGIES[item.effect]
        if strategy.apply_once and index < counter_state:
            continue
        _merge_into(ops, strategy.forward(item))

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
    pass

def build_ram_operations(items_received: list[int], counter_state: int,
                         checked_ids: set[int], to_reverse: set[int]) -> dict[int, RamOperation]:
    """Build every RAM operation of a tick, merged by address.

    Args:
        items_received: Ids of all received items, in reception order.
        counter_state: Number of items already applied (see ``_add_item_operations``).
        checked_ids: Ids of the locations already checked on the server.
        to_reverse: Ids of the locations whose vanilla item must be reversed.

    Returns:
        One operation per address, ready to be read, applied and written by the client.
    """
    ops: dict[int, RamOperation] = {}
    _add_item_operations(ops, items_received, counter_state)
    _add_location_resync_operations(ops, checked_ids)
    _add_location_reverse_operations(ops, to_reverse)
    return ops


