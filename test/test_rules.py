"""Unit tests for rules"""

from ..rules import *

# Templates to modify
class TestLocationRules(RaymanTestBase):
    def test_cage_requires_fist(self) -> None:
        """The first cage requires the Fist item."""
        self.assertAccessDependency(
            ["Dream Forest - Cage 1"],
            [["Fist"]],
            only_check_listed=True,
        )

    def test_cage_accepts_fist_or_magic_seed(self) -> None:
        """The second cage accepts either the Fist or Magic Seed."""
        self.assertAccessDependency(
            ["Blue Mountains - Cage 1"],
            [["Fist"], ["Magic Seed"]],
            only_check_listed=True,
        )
