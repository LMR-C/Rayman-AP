import logging

from ..items import ITEM_ID_TABLE
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


def build_item_operations(items_received: list[int], counter_state: int = 0) -> dict[int, RamOperation]:
    """Forward operations of the received items, merged by address.

    Args:
        items_received: Ids of all received items, in reception order.
        counter_state: Number of items already applied. Items of an ``apply_once``
            strategy with an index below it are skipped.
    """
    ops: dict[int, RamOperation] = {}
    for index, item_id in enumerate(items_received):
        item = ITEM_ID_TABLE.get(item_id)
        if item is None:
            logger.warning(f"Unknown id in ITEM_ID_TABLE: {item_id}")
            continue
        strategy = STRATEGIES[item.effect]
        if strategy.apply_once and index < counter_state:
            continue
        _merge_into(ops, strategy.forward(item))
    return ops
