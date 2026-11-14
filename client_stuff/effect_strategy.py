"""Per-effect strategy: forward and reverse RAM operations for each item type."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..items import ItemData
from ..utils import Effect
from .ram_operation import DeltaOperation, MaskOperation, RamOperation, SetOperation

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
        return [(address, MaskOperation(size=item.size.value, set_mask=item.mask)) for address in _addresses(item)]

    def reverse(self, item: ItemData) -> RamOps:
        return [(address, MaskOperation(size=item.size.value, clear_mask=item.mask)) for address in _addresses(item)]


class CounterStrategy(EffectStrategy):
    apply_once = True

    def forward(self, item: ItemData) -> RamOps:
        return [(address, self._delta(item, address, item.value)) for address in _addresses(item)]

    def reverse(self, item: ItemData) -> RamOps:
        return [(address, self._delta(item, address, -item.value)) for address in _addresses(item)]

    @staticmethod
    def _delta(item: ItemData, address: int, delta: int) -> DeltaOperation:
        return DeltaOperation(size=item.size.value, delta=delta, cap=_rule_for(address).cap)


class NoneStrategy(EffectStrategy):
    def forward(self, item: ItemData) -> RamOps:
        return []

    def reverse(self, item: ItemData) -> RamOps:
        return []


def _addresses(item: ItemData) -> tuple[int, ...]:
    """``item.address`` is either one address or a tuple of addresses in items.py."""
    return item.address if isinstance(item.address, tuple) else (item.address,)


class SetValueStrategy(EffectStrategy):
    """Write ``item.value`` at every address of the item (e.g. Big Power: HP and max HP)."""
    apply_once = True  # one-shot: re-applied on every tick it would lock the value (e.g. infinite HP)

    def forward(self, item: ItemData) -> RamOps:
        return [(address, SetOperation(size=item.size.value, value=item.value)) for address in _addresses(item)]

    def reverse(self, item: ItemData) -> RamOps:
        return []  # no vanilla location gives this kind of item yet


STRATEGIES: dict[Effect, EffectStrategy] = {
    Effect.BIT: BitStrategy(),
    Effect.COUNTER: CounterStrategy(),
    Effect.NONE: NoneStrategy(),
    Effect.SET_VALUE: SetValueStrategy(),
}
