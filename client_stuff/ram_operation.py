from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RamOperation(ABC):
    size: int

    @property
    def max_value(self) -> int:
        """Largest value that fits in ``size`` bytes."""
        return (1 << (8 * self.size)) - 1

    @abstractmethod
    def merge(self, other: "RamOperation") -> None:
        """Merge ``other`` into this operation, in place.

        Both operations target the same address. The result must be equivalent
        to applying ``self`` then ``other`` on the value read from RAM, so the
        client can do a single read/write per address.

        Args:
            other: Operation to merge, applied after ``self``.

        Raises:
            TypeError: If ``other`` is not the same kind of operation
                (masks and delta cannot be mixed on one address).
            ValueError: If ``other`` has a different ``size``, or incompatible
                parameters (see subclasses).
        """

    @abstractmethod
    def apply(self, read: int) -> int:
        """Compute the value to write from the value currently in RAM.

        Args:
            read: Current value at this address, read from RAM.

        Returns:
            The new value, always within ``0..max_value``.
        """

    def _check_mergeable(self, other: "RamOperation") -> None:
        if type(other) is not type(self):
            raise TypeError(f"Cannot merge {type(other).__name__} into {type(self).__name__}")
        if other.size != self.size:
            raise ValueError(f"Cannot merge operations of different sizes: {self.size} and {other.size}")


@dataclass
class MaskOperation(RamOperation):
    """Bit operation: ``(read & ~clear_mask) | set_mask``.

    Covers set bit (``set_mask``), clear bit (``clear_mask``) and set value
    (``clear_mask`` = all bits of the field, ``set_mask`` = value).
    A bit in both masks ends up set.
    """
    set_mask: int = 0
    clear_mask: int = 0

    def merge(self, other: RamOperation) -> None:
        """OR both masks. Merge order does not matter.

        At apply, clear happens before set, so a bit set by a received item
        always wins over a reverse that clears it.
        """
        self._check_mergeable(other)
        assert isinstance(other, MaskOperation)
        self.set_mask |= other.set_mask
        self.clear_mask |= other.clear_mask

    def apply(self, read: int) -> int:
        return ((read & ~self.clear_mask) | self.set_mask) & self.max_value


@dataclass
class DeltaOperation(RamOperation):
    """Counter operation: ``read + delta``, clamped to ``0..cap``.

    ``cap=None`` means the max value of ``size``. ``delta`` can be negative
    (reverse of a counter item).
    """
    delta: int = 0
    cap: int | None = None

    @property
    def upper_bound(self) -> int:
        return self.max_value if self.cap is None else min(self.cap, self.max_value)

    def merge(self, other: RamOperation) -> None:
        """Sum deltas. Both operations must share the same ``cap``.

        Note: clamping happens once at apply, so +5 then -5 merged gives 0,
        even if applying them one by one would have clamped in between.
        """
        self._check_mergeable(other)
        assert isinstance(other, DeltaOperation)
        if other.cap != self.cap:
            raise ValueError(f"Cannot merge operations with different caps: {self.cap} and {other.cap}")
        self.delta += other.delta

    def apply(self, read: int) -> int:
        return max(0, min(read + self.delta, self.upper_bound))


@dataclass
class SetOperation(RamOperation):
    """Write a fixed ``value``, whatever is currently in RAM."""
    value: int = 0

    def merge(self, other: RamOperation) -> None:
        """Same value twice is fine; two different values on one address is a conflict."""
        self._check_mergeable(other)
        assert isinstance(other, SetOperation)
        if other.value != self.value:
            raise ValueError(f"Cannot set two different values: {self.value} and {other.value}")

    def apply(self, read: int) -> int:
        return self.value & self.max_value


@dataclass(init=False)
class ReplaceIfOperation(RamOperation):
    """Write ``new`` only if RAM currently holds exactly ``expected``, otherwise leave it untouched."""
    expected: bytes
    new: bytes

    def __init__(self, expected: bytes, new: bytes) -> None:
        if len(expected) != len(new):
            raise ValueError(f"Cannot replace {len(expected)} bytes with {len(new)} bytes")
        self.size = len(expected)
        self.expected = expected
        self.new = new

    def merge(self, other: RamOperation) -> None:
        """Same replacement twice is fine; anything else on one address is a conflict."""
        self._check_mergeable(other)
        assert isinstance(other, ReplaceIfOperation)
        if other.expected != self.expected or other.new != self.new:
            raise ValueError(f"Cannot apply two different replacements: {self} and {other}")

    def apply(self, read: int) -> int:
        if read == int.from_bytes(self.expected, "little"):
            return int.from_bytes(self.new, "little")
        return read
