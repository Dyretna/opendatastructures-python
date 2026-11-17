"""Implementation-specific tests for MinStack.

Internals and extras unique to MinStack. The push/pop contract
is covered by tests/test_stack_ops.py (STACK_IMPLS) and the invariants
by test_invariants.py (seq).
"""

import pytest

from ods.arrays import MinStack


@pytest.fixture
def min_deque():
    return MinStack()


class TestRunningMinimum:
    def test_get_min_single_element(self, min_deque):
        min_deque.push(42)
        assert min_deque.get_min() == 42

    def test_get_min_tracks_running_minimum(self, min_deque):
        for v in [5, 3, 8, 1, 7]:
            min_deque.push(v)
        assert min_deque.get_min() == 1

    def test_get_min_ignores_pushed_larger_values(self, min_deque):
        min_deque.push(10)
        min_deque.push(20)
        min_deque.push(30)
        assert min_deque.get_min() == 10

    def test_min_updates_when_current_min_is_popped(self, min_deque):
        for v in [5, 3, 8, 1, 7]:
            min_deque.push(v)

        min_deque.pop()  # 7 — min unchanged
        assert min_deque.get_min() == 1

        min_deque.pop()  # 1 — min must move to 3
        assert min_deque.get_min() == 3

    def test_min_with_duplicate_minima(self, min_deque):
        min_deque.push(3)
        min_deque.push(3)
        min_deque.push(3)
        assert min_deque.get_min() == 3

        min_deque.pop()
        assert min_deque.get_min() == 3
        min_deque.pop()
        assert min_deque.get_min() == 3
        min_deque.pop()
        assert min_deque.is_empty()

    def test_min_recovery_after_full_drain(self, min_deque):
        min_deque.push(1)
        min_deque.pop()
        assert min_deque.is_empty()

        min_deque.push(10)
        assert min_deque.get_min() == 10


class TestPushPopSemantics:
    def test_pop_returns_last_pushed(self, min_deque):
        min_deque.push(10)
        min_deque.push(20)
        assert min_deque.pop() == 20
        assert min_deque.size == 1

    def test_pop_from_empty_raises(self, min_deque):
        assert min_deque.is_empty()
        with pytest.raises(IndexError):
            min_deque.pop()


class TestGetMinEmpty:
    def test_get_min_on_empty_raises(self, min_deque):
        assert min_deque.is_empty()
        with pytest.raises(IndexError):
            min_deque.get_min()


class TestGetAndIteration:
    def test_get_returns_bottom_to_top(self, min_deque):
        for v in [10, 20, 30]:
            min_deque.push(v)
        assert min_deque.get(0) == 10
        assert min_deque.get(2) == 30

    def test_get_out_of_bounds_raises(self, min_deque):
        min_deque.push(1)
        with pytest.raises(IndexError):
            min_deque.get(1)

    def test_iteration_is_bottom_to_top(self, min_deque):
        for v in [10, 20, 30]:
            min_deque.push(v)
        assert list(min_deque) == [10, 20, 30]

    def test_iteration_does_not_mutate(self, min_deque):
        for v in [1, 2, 3]:
            min_deque.push(v)
        list(min_deque)
        assert min_deque.size == 3
        assert min_deque.get_min() == 1


class TestSizeBookkeeping:
    def test_size_tracks_push_and_pop(self, min_deque):
        assert min_deque.size == 0
        min_deque.push(1)
        min_deque.push(2)
        assert min_deque.size == 2
        min_deque.pop()
        assert min_deque.size == 1
        min_deque.pop()
        assert min_deque.size == 0
