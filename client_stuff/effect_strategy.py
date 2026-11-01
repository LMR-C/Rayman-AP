"""Per-effect strategy: forward and reverse RAM operations for each item type."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..items import ItemData
from ..utils import Effect
from .ram_operation import DeltaOperation, MaskOperation, RamOperation

RamOps = list[tuple[int, RamOperation]]  # (address, operation)


@dataclass(frozen=True)
class CounterRule:
    """RAM-side limits of a counter address.

    cap: max value written (None = max of the block size).
    """
    cap: int | None = None


COUNTER_RULES: dict[int, CounterRule] = {
    0x1E4D50: CounterRule(cap=99),  # Life counter
}

DEFAULT_COUNTER_RULE = CounterRule()


def _rule_for(address: int) -> CounterRule:
    return COUNTER_RULES.get(address, DEFAULT_COUNTER_RULE)


class EffectStrategy(ABC):
    apply_once: bool = False  # True: each received item must be applied only once (tracked by counter)

    @abstractmethod
    def forward(self, item: ItemData) -> RamOps:
        """Operations giving ``item`` to the player."""

    @abstractmethod
    def reverse(self, item: ItemData) -> RamOps:
        """Operations cancelling ``item`` when the game gave it (vanilla location)."""


class BitStrategy(EffectStrategy):
    def forward(self, item: ItemData) -> RamOps:
        return [(item.address, MaskOperation(size=item.size.value, set_mask=item.value))]

    def reverse(self, item: ItemData) -> RamOps:
        return [(item.address, MaskOperation(size=item.size.value, clear_mask=item.value))]


class CounterStrategy(EffectStrategy):
    apply_once = True

    def forward(self, item: ItemData) -> RamOps:
        return [(item.address, self._delta(item, item.value))]

    def reverse(self, item: ItemData) -> RamOps:
        return [(item.address, self._delta(item, -item.value))]

    @staticmethod
    def _delta(item: ItemData, delta: int) -> DeltaOperation:
        # ItemData.__post_init__ guarantees an address for COUNTER items
        return DeltaOperation(size=item.size.value, delta=delta, cap=_rule_for(item.address).cap)


class NoneStrategy(EffectStrategy):
    def forward(self, item: ItemData) -> RamOps:
        return []

    def reverse(self, item: ItemData) -> RamOps:
        return []


STRATEGIES: dict[Effect, EffectStrategy] = {
    Effect.BIT: BitStrategy(),
    Effect.COUNTER: CounterStrategy(),
    Effect.NONE: NoneStrategy(),
}
