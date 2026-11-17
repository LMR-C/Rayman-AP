"""Per-effect strategy: forward and reverse RAM operations for each item type."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

from ..items import ItemData
from ..utils import Effect
from .ram_map import HP_ADDRESS, HP_MAX_ADDRESS
from .ram_operation import DeltaOperation, MaskOperation, RamOperation, SetOperation

logger = logging.getLogger("EffectStrategy")

RamOps = list[tuple[int, RamOperation]]  # (address, operation)


@dataclass(frozen=True)
class CounterRule:
    """RAM-side limits of a counter address.

    cap: fixed max value written (None = max of the block size).
    cap_from: address whose current value is the max (resolved per tick by operation_builder).
    """
    cap: int | None = None
    cap_from: int | None = None


COUNTER_RULES: dict[int, CounterRule] = {
    0x1E4D50: CounterRule(cap=99),  # Life counter
    HP_ADDRESS: CounterRule(cap_from=HP_MAX_ADDRESS),  # HP, bounded by max HP
}

DEFAULT_COUNTER_RULE = CounterRule()


def rule_for(address: int) -> CounterRule:
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
        return DeltaOperation(size=item.size.value, delta=delta, cap=rule_for(address).cap)


class NoneStrategy(EffectStrategy):
    def forward(self, item: ItemData) -> RamOps:
        return []

    def reverse(self, item: ItemData) -> RamOps:
        return []


def _addresses(item: ItemData) -> tuple[int, ...]:
    """``item.address`` is either one address or a tuple of addresses in items.py."""
    return item.address if isinstance(item.address, tuple) else (item.address,)


class SetValueStrategy(EffectStrategy):
    """Write ``item.value`` at every address of the item."""
    apply_once = True  # one-shot: re-applied on every tick it would lock the value (e.g. infinite HP)

    def forward(self, item: ItemData) -> RamOps:
        return [(address, SetOperation(size=item.size.value, value=item.value)) for address in _addresses(item)]

    def reverse(self, item: ItemData) -> RamOps:
        return []  # no vanilla location gives this kind of item yet


class RaiseMaxStrategy(EffectStrategy):
    """Raise a max and refill the counter it bounds (e.g. Big Power: HP and max HP).

    Among ``item.address``, an address whose rule has ``cap_from`` is the counter (delta of
    ``item.value``, capped later by operation_builder); the others are maxes (set to ``item.value``).
    """
    apply_once = True

    def forward(self, item: ItemData) -> RamOps:
        addresses = _addresses(item)
        for address in addresses:
            cap_from = rule_for(address).cap_from
            if cap_from is not None and cap_from not in addresses:
                logger.warning(f"{item.name}: refills {address:#x} but does not set its max {cap_from:#x}")
        size = item.size.value
        return [(address, self._op(address, size, item.value)) for address in addresses]

    @staticmethod
    def _op(address: int, size: int, value: int) -> RamOperation:
        if rule_for(address).cap_from is not None:
            return DeltaOperation(size=size, delta=value)  # refill: HP >= 0, so read + value reaches the max
        return SetOperation(size=size, value=value)

    def reverse(self, item: ItemData) -> RamOps:
        # No vanilla location gives this item. A reverse could not be exact anyway: the Set does not
        # keep the old max, and the refill does not know how many HP the cap really gave.
        return []


STRATEGIES: dict[Effect, EffectStrategy] = {
    Effect.BIT: BitStrategy(),
    Effect.COUNTER: CounterStrategy(),
    Effect.NONE: NoneStrategy(),
    Effect.SET_VALUE: SetValueStrategy(),
    Effect.RAISE_MAX: RaiseMaxStrategy(),
}
