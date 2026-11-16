"""Index-contract tests: get / set / add(i, x) / remove(i).

Runs against every class registered in INDEX_IMPLS
(tests/implementations.py), via the `index_seq` fixture in conftest.py.

Intentionally excluded from INDEX_IMPLS:
  * OrderedDeque  - pure deque contract only (test_deque_ops.py)
  * BoundedDeque  - fixed capacity, has its own module
  * DLList        - uses BoundedDeque
  * SEList        - uses BoundedDeque
  * sets (SkiplistSSet etc.) - no positional add/remove

Covered elsewhere:
  * size/is_empty invariants   -> test_invariants.py
  * deque facade operations    -> test_deque_ops.py
  * implementation internals   -> per-implementation modules
"""

import random

import pytest
from helpers import build, build_last, contents


class TestAdd:
    def test_add_into_empty(self, index_seq):
        index_seq.add(0, "a")
        assert index_seq.size == 1
        assert contents(index_seq) == ["a"]

    def test_add_at_front(self, index_seq):
        build(index_seq, [1, 2, 3])
        index_seq.add(0, 0)
        assert contents(index_seq) == [0, 1, 2, 3]

    def test_add_at_end(self, index_seq):
        build(index_seq, [1, 2, 3])
        index_seq.add(index_seq.size, 4)
        assert contents(index_seq) == [1, 2, 3, 4]

    def test_add_in_middle(self, index_seq):
        build(index_seq, [1, 2, 4, 5])
        index_seq.add(2, 3)
        assert contents(index_seq) == [1, 2, 3, 4, 5]

    def test_add_increments_size_by_one(self, index_seq):
        build(index_seq, [1, 2, 3])
        before = index_seq.size
        index_seq.add(1, 99)
        assert index_seq.size == before + 1

    def test_add_at_every_position(self, index_seq):
        for i in range(4):
            fresh = type(index_seq)()
            build(fresh, [1, 2, 3])
            fresh.add(i, 99)
            expected = [1, 2, 3]
            expected.insert(i, 99)
            assert contents(fresh) == expected

    def test_add_then_remove_same_index_restores_state(self, index_seq):
        build(index_seq, [1, 2, 3, 4])
        before = contents(index_seq)
        for i in range(len(before) + 1):
            index_seq.add(i, 99)
            assert index_seq.remove(i) == 99
            assert contents(index_seq) == before

    def test_add_near_front_and_near_back(self, index_seq):
        """Exercises both shift directions inside add()."""
        build(index_seq, list(range(10)))
        index_seq.add(1, "L")
        index_seq.add(index_seq.size - 1, "R")
        expected = list(range(10))
        expected.insert(1, "L")
        expected.insert(len(expected) - 1, "R")
        assert contents(index_seq) == expected

    def test_add_after_removals_from_front(self, index_seq):
        """Shift the logical window, then insert at the front."""
        build(index_seq, [1, 2, 3, 4, 5, 6])
        for _ in range(3):
            index_seq.remove(0)
        assert contents(index_seq) == [4, 5, 6]
        index_seq.add(0, 3)
        index_seq.add(0, 2)
        assert contents(index_seq) == [2, 3, 4, 5, 6]

    def test_add_triggers_growth(self, index_seq):
        for i in range(500):
            index_seq.add(0, i)
        assert index_seq.size == 500
        assert contents(index_seq) == list(reversed(range(500)))

    @pytest.mark.parametrize("bad_index", [-1, 5])
    def test_add_out_of_bounds_raises(self, index_seq, bad_index):
        build(index_seq, [1, 2, 3, 4])
        with pytest.raises(IndexError):
            index_seq.add(bad_index, 99)


class TestRemove:
    def test_remove_at_front(self, index_seq):
        build(index_seq, [1, 2, 3])
        assert index_seq.remove(0) == 1
        assert contents(index_seq) == [2, 3]

    def test_remove_at_end(self, index_seq):
        build(index_seq, [1, 2, 3])
        assert index_seq.remove(index_seq.size - 1) == 3
        assert contents(index_seq) == [1, 2]

    def test_remove_in_middle(self, index_seq):
        build(index_seq, [1, 2, 3, 4, 5])
        assert index_seq.remove(2) == 3
        assert contents(index_seq) == [1, 2, 4, 5]

    def test_remove_decrements_size_by_one(self, index_seq):
        build(index_seq, [1, 2, 3])
        before = index_seq.size
        index_seq.remove(1)
        assert index_seq.size == before - 1

    def test_remove_returns_removed_value(self, index_seq):
        build(index_seq, [10, 20, 30])
        assert index_seq.remove(1) == 20

    def test_remove_only_element(self, index_seq):
        index_seq.add(0, 42)
        assert index_seq.remove(0) == 42
        assert index_seq.size == 0
        assert index_seq.is_empty()

    def test_remove_at_every_position(self, index_seq):
        baseline = [1, 2, 3, 4, 5]
        for i in range(len(baseline)):
            fresh = type(index_seq)()
            build(fresh, baseline)
            expected = list(baseline)
            expected.pop(i)
            assert fresh.remove(i) == baseline[i]
            assert contents(fresh) == expected

    def test_remove_near_front_and_near_back(self, index_seq):
        """Exercises both shift directions inside remove()."""
        build(index_seq, list(range(10)))
        assert index_seq.remove(1) == 1
        assert index_seq.remove(index_seq.size - 1) == 9
        assert contents(index_seq) == [0, 2, 3, 4, 5, 6, 7, 8]

    def test_remove_from_front_drains_in_order(self, index_seq):
        build(index_seq, list(range(10)))
        for expected in range(10):
            assert index_seq.remove(0) == expected
        assert index_seq.is_empty()

    def test_remove_from_back_drains_in_reverse(self, index_seq):
        build(index_seq, list(range(10)))
        for expected in reversed(range(10)):
            assert index_seq.remove(index_seq.size - 1) == expected
        assert index_seq.is_empty()

    def test_remove_from_empty_raises(self, index_seq):
        assert index_seq.is_empty()
        with pytest.raises(IndexError):
            index_seq.remove(0)

    @pytest.mark.parametrize("bad_index", [-1, 4])
    def test_remove_out_of_bounds_raises(self, index_seq, bad_index):
        build(index_seq, [1, 2, 3, 4])
        with pytest.raises(IndexError):
            index_seq.remove(bad_index)

    def test_remove_triggers_shrink(self, index_seq):
        build(index_seq, list(range(200)))
        for _ in range(190):
            index_seq.remove(0)
        assert index_seq.size == 10
        assert contents(index_seq) == list(range(190, 200))


class TestGetSet:
    def test_get_at_each_position(self, index_seq):
        build(index_seq, [10, 20, 30, 40])
        assert index_seq.get(0) == 10
        assert index_seq.get(2) == 30
        assert index_seq.get(3) == 40

    def test_get_out_of_bounds_raises(self, index_seq):
        build(index_seq, [1, 2, 3, 4])
        with pytest.raises(IndexError):
            index_seq.get(10)

    def test_set_returns_old_value(self, index_seq):
        build(index_seq, [10, 20, 30])
        old = index_seq.set(1, 99)
        assert old == 20
        assert index_seq.get(1) == 99
        assert contents(index_seq) == [10, 99, 30]

    def test_set_preserves_others(self, index_seq):
        build(index_seq, [1, 2, 3, 4, 5])
        index_seq.set(2, 99)
        assert contents(index_seq) == [1, 2, 99, 4, 5]

    def test_set_out_of_bounds_raises(self, index_seq):
        build(index_seq, [1, 2, 3, 4])
        with pytest.raises(IndexError):
            index_seq.set(10, 99)


class TestMixedOps:
    def test_add_then_remove_alternating(self, index_seq):
        build(index_seq, [1, 2, 3])
        index_seq.add(0, 0)
        assert index_seq.remove(index_seq.size - 1) == 3
        index_seq.add(index_seq.size, 4)
        assert index_seq.remove(0) == 0
        assert contents(index_seq) == [1, 2, 4]

    def test_queue_pattern(self, index_seq):
        """add at end, remove at front."""
        for i in range(50):
            index_seq.add(index_seq.size, i)
        for expected in range(50):
            assert index_seq.remove(0) == expected
        assert index_seq.is_empty()

    def test_stack_pattern(self, index_seq):
        """add at end, remove at end."""
        for i in range(50):
            index_seq.add(index_seq.size, i)
        for expected in reversed(range(50)):
            assert index_seq.remove(index_seq.size - 1) == expected
        assert index_seq.is_empty()

    def test_repeated_grow_and_shrink_cycles(self, index_seq):
        for _ in range(5):
            for i in range(100):
                index_seq.add(index_seq.size, i)
            assert index_seq.size == 100
            for _ in range(100):
                index_seq.remove(index_seq.size - 1)
            assert index_seq.size == 0
            assert index_seq.is_empty()

    def test_capacity_never_below_size(self, index_seq):
        if not hasattr(index_seq, "capacity"):
            pytest.skip("implementation exposes no capacity")

        rng = random.Random(7)
        for _ in range(500):
            if index_seq.size == 0 or rng.random() < 0.6:
                index_seq.add(rng.randint(0, index_seq.size), rng.randint(0, 99))
            else:
                index_seq.remove(rng.randrange(index_seq.size))
            assert index_seq.capacity >= index_seq.size

    def test_random_operations_match_reference_list(self, index_seq):
        rng = random.Random(20261018)
        ref = []

        for step in range(600):
            if not ref or rng.random() < 0.55:
                i = rng.randint(0, len(ref))
                v = rng.randint(0, 999)
                index_seq.add(i, v)
                ref.insert(i, v)
            else:
                i = rng.randrange(len(ref))
                assert index_seq.remove(i) == ref.pop(i)

            assert index_seq.size == len(ref)

            # full comparison is O(n); sample it instead of every step
            if step % 89 == 0:
                assert contents(index_seq) == ref

        assert contents(index_seq) == ref

    def test_build_last_matches_reference(self, index_seq):
        """add_last must behave exactly like list.append."""
        values = list(range(25))
        build_last(index_seq, values)
        assert contents(index_seq) == values
