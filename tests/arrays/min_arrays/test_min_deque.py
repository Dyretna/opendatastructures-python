"""Implementation-specific tests for MinDeque.

Internals and extras unique to MinDeque. The deque facade
contract (add_first/add_last/remove_first/remove_last) is covered by
tests/test_deque_ops.py (PURE_DEQUE_IMPLS) and the invariants by
test_invariants.py (seq).
"""

import random

import pytest
from helpers import build_last, drain_first

from ods.arrays import MinDeque


@pytest.fixture
def min_deque():
    return MinDeque()


class TestDequeFacadeSemantics:
    def test_add_last_then_remove_first_is_fifo(self, min_deque):
        build_last(min_deque, [10, 20, 30])
        assert min_deque.remove_first() == 10
        assert min_deque.size == 2

    def test_add_last_then_remove_last_is_lifo(self, min_deque):
        build_last(min_deque, [10, 20, 30])
        assert min_deque.remove_last() == 30
        assert min_deque.size == 2

    def test_mixed_adds_preserve_order(self, min_deque):
        min_deque.add_last(1)
        min_deque.add_first(0)
        min_deque.add_last(2)
        min_deque.add_first(-1)
        assert drain_first(min_deque) == [-1, 0, 1, 2]

    def test_remove_first_from_empty_raises(self, min_deque):
        assert min_deque.size == 0
        with pytest.raises(IndexError):
            min_deque.remove_first()

    def test_remove_last_from_empty_raises(self, min_deque):
        with pytest.raises(IndexError):
            min_deque.remove_last()

    def test_single_element_roundtrip_both_ends(self, min_deque):
        min_deque.add_last(42)
        assert min_deque.remove_last() == 42
        assert min_deque.size == 0

        min_deque.add_first(43)
        assert min_deque.remove_first() == 43
        assert min_deque.size == 0


class TestRunningMinimum:
    def test_get_min_single_element(self, min_deque):
        min_deque.add_last(42)
        assert min_deque.get_min() == 42

    def test_get_min_tracks_minimum_whole_deque(self, min_deque):
        min_deque.add_last(5)
        min_deque.add_last(3)
        min_deque.add_first(8)
        min_deque.add_first(1)
        min_deque.add_last(7)
        assert min_deque.get_min() == 1

    def test_min_updates_from_both_ends(self, min_deque):
        min_deque.add_last(5)
        min_deque.add_last(1)
        min_deque.add_first(3)

        assert min_deque.get_min() == 1

        min_deque.remove_last()  # 1 was the min, popped from back
        assert min_deque.get_min() == 3

        min_deque.remove_first()  # 3 was the min, popped from front
        assert min_deque.get_min() == 5

    def test_min_with_min_in_the_middle(self, min_deque):
        min_deque.add_last(4)
        min_deque.add_last(2)  # min sits between the stacks after balance
        min_deque.add_last(6)
        min_deque.add_last(8)
        min_deque.add_last(9)

        assert min_deque.get_min() == 2

        min_deque.remove_first()  # 4
        min_deque.remove_first()  # 2 — min leaves from the front side
        assert min_deque.get_min() == 6

    def test_min_survives_rebalancing(self, min_deque):
        """_balance() rebuilds both stacks; min bookkeeping must survive it."""
        rng = random.Random(99)
        ref = []

        for step in range(200):
            if not ref or rng.random() < 0.55:
                v = rng.randint(0, 999)
                if rng.random() < 0.5:
                    min_deque.add_first(v)
                    ref.insert(0, v)
                else:
                    min_deque.add_last(v)
                    ref.append(v)
            else:
                if rng.random() < 0.5:
                    assert min_deque.remove_first() == ref.pop(0)
                else:
                    assert min_deque.remove_last() == ref.pop(-1)

            assert min_deque.size == len(ref)
            if ref:
                assert min_deque.get_min() == min(ref)
            else:
                with pytest.raises(IndexError):
                    min_deque.get_min()

        assert drain_first(min_deque) == ref

    def test_get_min_on_empty_raises(self, min_deque):
        with pytest.raises(IndexError):
            min_deque.get_min()

    def test_get_min_after_full_drain_and_refill(self, min_deque):
        min_deque.add_last(1)
        min_deque.remove_last()
        min_deque.add_last(10)
        assert min_deque.get_min() == 10

    def test_min_with_duplicate_minima_both_sides(self, min_deque):
        min_deque.add_first(3)
        min_deque.add_last(3)
        assert min_deque.get_min() == 3

        min_deque.remove_last()
        assert min_deque.get_min() == 3
        min_deque.remove_first()
        assert min_deque.size == 0


class TestGetAndIteration:
    def test_get_front_and_back(self, min_deque):
        min_deque.add_last(10)
        min_deque.add_last(20)
        min_deque.add_last(30)
        assert min_deque.get(0) == 10
        assert min_deque.get(1) == 20
        assert min_deque.get(2) == 30

    def test_get_after_front_heavy_load(self, min_deque):
        for i in range(5):
            min_deque.add_first(i)  # contents: 4, 3, 2, 1, 0
        assert min_deque.get(0) == 4
        assert min_deque.get(4) == 0

    def test_get_out_of_bounds_raises(self, min_deque):
        min_deque.add_last(1)
        with pytest.raises(IndexError):
            min_deque.get(1)

    def test_iteration_is_front_to_back(self, min_deque):
        min_deque.add_last(10)
        min_deque.add_last(20)
        min_deque.add_first(5)
        min_deque.add_last(30)
        assert list(min_deque) == [5, 10, 20, 30]

    def test_iteration_across_rebalance_boundary(self, min_deque):
        """Elements on both sides of the split must appear in logical order."""
        for v in [1, 2, 3, 4, 5]:
            min_deque.add_last(v)
        min_deque.remove_first()  # triggers rebalancing on the way
        min_deque.add_last(6)
        assert list(min_deque) == [2, 3, 4, 5, 6]

    def test_iteration_does_not_mutate(self, min_deque):
        build_last(min_deque, [1, 2, 3])
        list(min_deque)
        assert min_deque.size == 3
        assert min_deque.get_min() == 1


class TestBalanceBehaviour:
    def test_balance_keeps_sizes_consistent(self, min_deque):
        """After heavy one-sided loading, front+back must equal size."""
        for i in range(100):
            min_deque.add_last(i)

        for _ in range(50):
            min_deque.remove_first()

        for i in range(100, 150):
            min_deque.add_first(i)

        assert min_deque.size == 100
        assert min_deque.get_min() == 50

    def test_repeated_grow_shrink_cycles_keep_min(self, min_deque):
        for _ in range(5):
            for i in range(50):
                min_deque.add_last(i)
            assert min_deque.size == 50
            assert min_deque.get_min() == 0

            for _ in range(50):
                min_deque.remove_last()
            assert min_deque.size == 0
