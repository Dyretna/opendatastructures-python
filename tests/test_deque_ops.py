"""Deque-contract tests: add_first / add_last / remove_first / remove_last.

Runs against every class registered in PURE_DEQUE_IMPLS
(tests/implementations.py), via the `deque_seq` fixture in conftest.py.

Covered elsewhere:
  * size/is_empty invariants      -> test_invariants.py (`seq`, all impls)
  * get/set/add(i, x)/remove(i)   -> test_index_ops.py (`index_seq`)
  * implementation internals      -> per-implementation modules

"""

import random

import pytest
from helpers import build_last, drain_first, drain_last


class TestAddFirstAddLast:
    def test_add_last_appends(self, deque_seq):
        build_last(deque_seq, [1, 2, 3])
        assert drain_first(deque_seq) == [1, 2, 3]

    def test_add_first_prepends(self, deque_seq):
        deque_seq.add_first(1)
        deque_seq.add_first(2)
        deque_seq.add_first(3)
        assert drain_first(deque_seq) == [3, 2, 1]

    def test_mixed_add_operations_preserve_order(self, deque_seq):
        deque_seq.add_last(1)
        deque_seq.add_first(0)
        deque_seq.add_last(2)
        deque_seq.add_first(-1)
        assert drain_first(deque_seq) == [-1, 0, 1, 2]

    def test_add_first_with_large_batch(self, deque_seq):
        for i in range(100):
            deque_seq.add_first(i)
        assert deque_seq.size == 100
        assert drain_first(deque_seq) == list(reversed(range(100)))

    def test_add_last_with_large_batch(self, deque_seq):
        for i in range(100):
            deque_seq.add_last(i)
        assert deque_seq.size == 100
        assert drain_last(deque_seq) == list(reversed(range(100)))


class TestRemoveFirstRemoveLast:
    def test_remove_first_returns_front_element(self, deque_seq):
        build_last(deque_seq, [0, 1, 2, 3, 4])
        assert deque_seq.remove_first() == 0
        assert deque_seq.size == 4
        assert drain_first(deque_seq) == [1, 2, 3, 4]

    def test_remove_last_returns_back_element(self, deque_seq):
        build_last(deque_seq, [0, 1, 2, 3, 4])
        assert deque_seq.remove_last() == 4
        assert deque_seq.size == 4
        assert drain_first(deque_seq) == [0, 1, 2, 3]

    def test_remove_first_from_single_element(self, deque_seq):
        deque_seq.add_last(42)
        assert deque_seq.remove_first() == 42
        assert deque_seq.is_empty()

    def test_remove_last_from_single_element(self, deque_seq):
        deque_seq.add_first(42)
        assert deque_seq.remove_last() == 42
        assert deque_seq.is_empty()

    def test_alternating_remove_operations(self, deque_seq):
        build_last(deque_seq, list(range(6)))
        assert deque_seq.remove_first() == 0
        assert deque_seq.remove_last() == 5
        assert deque_seq.remove_first() == 1
        assert deque_seq.remove_last() == 4
        assert deque_seq.remove_first() == 2
        assert deque_seq.remove_last() == 3
        assert deque_seq.is_empty()

    def test_remove_first_drains_in_order(self, deque_seq):
        build_last(deque_seq, list(range(10)))
        for expected in range(10):
            assert deque_seq.remove_first() == expected
        assert deque_seq.is_empty()

    def test_remove_last_drains_in_reverse(self, deque_seq):
        build_last(deque_seq, list(range(10)))
        for expected in reversed(range(10)):
            assert deque_seq.remove_last() == expected
        assert deque_seq.is_empty()


class TestEdgeCases:
    def test_remove_first_from_empty_raises(self, deque_seq):
        assert deque_seq.is_empty()
        with pytest.raises(IndexError):
            deque_seq.remove_first()

    def test_remove_last_from_empty_raises(self, deque_seq):
        assert deque_seq.is_empty()
        with pytest.raises(IndexError):
            deque_seq.remove_last()

    def test_add_and_remove_single_element_repeatedly(self, deque_seq):
        for _ in range(10):
            deque_seq.add_first(1)
            assert deque_seq.remove_first() == 1
            assert deque_seq.is_empty()

    def test_mixed_add_remove_with_final_state_check(self, deque_seq):
        """Add 5 from front, remove 3 from back, add 2 from back."""
        for i in range(5):
            deque_seq.add_first(i)

        # contents are now: 4, 3, 2, 1, 0
        assert deque_seq.remove_last() == 0
        assert deque_seq.remove_last() == 1
        assert deque_seq.remove_last() == 2

        deque_seq.add_last(10)
        deque_seq.add_last(11)

        assert deque_seq.size == 4
        assert drain_first(deque_seq) == [4, 3, 10, 11]


class TestGrowthShrinkageBehavior:
    def test_growth_after_many_add_first(self, deque_seq):
        for i in range(1000):
            deque_seq.add_first(i)
        assert deque_seq.size == 1000
        assert not deque_seq.is_empty()

    def test_growth_after_many_add_last(self, deque_seq):
        for i in range(1000):
            deque_seq.add_last(i)
        assert deque_seq.size == 1000
        assert not deque_seq.is_empty()

    def test_shrinkage_after_many_remove_first(self, deque_seq):
        build_last(deque_seq, list(range(1000)))
        for _ in range(900):
            deque_seq.remove_first()
        assert deque_seq.size == 100
        assert drain_first(deque_seq) == list(range(900, 1000))

    def test_shrinkage_after_many_remove_last(self, deque_seq):
        build_last(deque_seq, list(range(1000)))
        for _ in range(900):
            deque_seq.remove_last()
        assert deque_seq.size == 100
        assert drain_last(deque_seq) == list(reversed(range(100)))


class TestRoundtripConsistency:
    def test_add_first_then_remove_first_roundtrip(self, deque_seq):
        for v in [5, 4, 3, 2, 1]:
            deque_seq.add_first(v)
        # contents: 1, 2, 3, 4, 5
        for expected in [1, 2, 3, 4, 5]:
            assert deque_seq.remove_first() == expected

    def test_add_last_then_remove_last_roundtrip(self, deque_seq):
        for v in [1, 2, 3, 4, 5]:
            deque_seq.add_last(v)
        for expected in reversed([1, 2, 3, 4, 5]):
            assert deque_seq.remove_last() == expected

    def test_fifo_behavior_via_add_last_remove_first(self, deque_seq):
        """add_last then remove_first drains in insertion order."""
        values = [10, 20, 30, 40, 50]
        for v in values:
            deque_seq.add_last(v)
        for expected in values:
            assert deque_seq.remove_first() == expected

    def test_fifo_behavior_via_add_first_remove_last(self, deque_seq):
        """add_first then remove_last drains in insertion order."""
        values = [10, 20, 30, 40, 50]
        for v in values:
            deque_seq.add_first(v)
        for expected in values:
            assert deque_seq.remove_last() == expected

    def test_lifo_behavior_via_add_last_remove_last(self, deque_seq):
        """add_last then remove_last drains in reverse insertion order."""
        values = [10, 20, 30, 40, 50]
        for v in values:
            deque_seq.add_last(v)
        for expected in reversed(values):
            assert deque_seq.remove_last() == expected

    def test_lifo_behavior_via_add_first_remove_first(self, deque_seq):
        """add_first then remove_first drains in reverse insertion order."""
        values = [10, 20, 30, 40, 50]
        for v in values:
            deque_seq.add_first(v)
        for expected in reversed(values):
            assert deque_seq.remove_first() == expected


class TestRandomizedStress:
    def test_random_operations_stress(self, deque_seq):
        """Random mix of adds and removes, verified against a list mirror."""
        rng = random.Random(42)
        reference = []

        for _ in range(500):
            op = rng.choice(["add_first", "add_last", "remove_first", "remove_last"])

            if op == "add_first":
                value = rng.randint(0, 1000)
                deque_seq.add_first(value)
                reference.insert(0, value)
            elif op == "add_last":
                value = rng.randint(0, 1000)
                deque_seq.add_last(value)
                reference.append(value)
            elif op == "remove_first" and reference:
                assert deque_seq.remove_first() == reference.pop(0)
            elif op == "remove_last" and reference:
                assert deque_seq.remove_last() == reference.pop(-1)

            assert deque_seq.size == len(reference)

        assert drain_first(deque_seq) == reference
