import logging
from dataclasses import dataclass

from .items import ITEM_ID_TABLE
from .utils import Effect

logger = logging.getLogger("RamOperation")

@dataclass
class RamOperation:
    effect: Effect
    size: int
    value: int
    cap: int | None = None
    overflow_step : int | None = None

    def merge(self, value: int) -> None:
        match self.effect:
            case Effect.SET_BIT:
                self.value |= value
            case Effect.ADD:
                self.value += value
            case Effect.SET_VALUE:
                self.value = value
            case _:
                raise ValueError(f"Unhandled effect : {self.effect}")

    def apply(self, read: int) -> tuple[int, int]:
        """Compute the value to write from the value currently in RAM.

        Args:
            read: Current value at this address, read from RAM.

        Returns:
            (new_value, overflow). ``overflow`` is the amount to merge into the
            overflow address (ADD with ``overflow_step``), 0 otherwise.

        Raises:
            ValueError: If ``effect`` is not handled.
        """
        match self.effect:
            case Effect.SET_BIT:
                return read | self.value, 0

            case Effect.ADD:
                total = read + self.value
                if self.overflow_step is not None:
                    return total % self.overflow_step, total // self.overflow_step
                if self.cap is not None:
                    return min(total, self.cap), 0
                return total, 0

            case Effect.SET_VALUE:
                return self.value, 0

            case _:
                raise ValueError(f"Unhandled effect : {self.effect}")


def build_item_operations(item_ids: list[int], applied_count: int = 0) -> dict[int, RamOperation]:
    operations: dict[int, RamOperation] = {}
    for index, item_id in enumerate(item_ids):
        item = ITEM_ID_TABLE.get(item_id)
        if item is None :
            logger.warning(f"ID {item_id} doesn't exist in ITEM_ID_TABLE")
            continue
        if item.address is None or (item.effect == Effect.ADD and index < applied_count):
            continue

        op = operations.get(item.address)
        if op is None :
            operations[item.address]=RamOperation(item.effect,item.size.value,item.value)
        else:
            if item.effect != op.effect:
                logger.error(
                f"Two different operation for same address, address:{item.address}, "
                f"item.effect: {item.effect}, op.effect: {op.effect}"
                )
                continue
            op.merge(item.value)

    return operations

def build_reverse_default_operations():
    pass
