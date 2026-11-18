# tests/arrays/deque/test_bounded_deque.py

import pytest

from ods.arrays import BoundedDeque


def contents(dq):
    return [dq.get(i) for i in range(dq.size)]


class TestConstruction:
    def test_default_capacity_is_positive(self):
        dq = BoundedDeque()

        assert dq.capacity > 0
        assert dq.size == 0

    def test_requested_capacity_allocates_one_spare_slot(self):
        dq = BoundedDeque(b=5)

        assert len(dq.a) == 6
        assert dq.capacity == 6

    def test_starts_empty(self):
        dq = BoundedDeque(b=8)

        assert dq.is_empty()
        assert dq.size == 0


class TestCapacityLimits:
    def test_fill_to_capacity_succeeds(self):
        dq = BoundedDeque(b=3)

        for i in range(dq.capacity):
            dq.add_last(i)

        assert dq.size == dq.capacity

    def test_add_last_when_full_raises(self):
        dq = BoundedDeque(b=3)

        for i in range(dq.capacity):
            dq.add_last(i)

        with pytest.raises(ValueError):
            dq.add_last(99)

    def test_add_first_when_full_raises(self):
        dq = BoundedDeque(b=3)

        for i in range(dq.capacity):
            dq.add_last(i)

        with pytest.raises(ValueError):
            dq.add_first(99)

    def test_add_middle_when_full_raises(self):
        dq = BoundedDeque(b=3)

        for i in range(dq.capacity):
            dq.add_last(i)

        with pytest.raises(ValueError):
            dq.add(1, 99)

    def test_no_resize_occurs_during_fill(self):
        dq = BoundedDeque(b=20)

        original_capacity = dq.capacity

        for i in range(original_capacity):
            dq.add_last(i)

        assert dq.capacity == original_capacity


class TestReuseFreedSpace:
    def test_remove_first_frees_capacity(self):
        dq = BoundedDeque(b=4)

        for i in range(dq.capacity):
            dq.add_last(i)

        dq.remove_first()
        dq.add_last(99)

        assert dq.size == dq.capacity

    def test_remove_last_frees_capacity(self):
        dq = BoundedDeque(b=4)

        for i in range(dq.capacity):
            dq.add_last(i)

        dq.remove_last()
        dq.add_last(99)

        assert dq.size == dq.capacity

    def test_multiple_removals_allow_multiple_insertions(self):
        dq = BoundedDeque(b=5)

        for i in range(dq.capacity):
            dq.add_last(i)

        dq.remove_first()
        dq.remove_first()

        dq.add_last(10)
        dq.add_last(11)

        assert contents(dq) == [2, 3, 4, 5, 10, 11]


class TestWraparound:
    def test_wraparound_with_add_last(self):
        dq = BoundedDeque(b=5)

        for i in range(5):
            dq.add_last(i)

        dq.remove_first()
        dq.remove_first()

        dq.add_last(5)
        dq.add_last(6)

        assert contents(dq) == [2, 3, 4, 5, 6]

    def test_wraparound_with_add_first(self):
        dq = BoundedDeque(b=5)

        for i in range(5):
            dq.add_last(i)

        dq.remove_last()
        dq.remove_last()

        dq.add_first(-1)
        dq.add_first(-2)

        assert contents(dq) == [-2, -1, 0, 1, 2]

    def test_wraparound_preserves_order_after_many_operations(self):
        dq = BoundedDeque(b=8)

        for i in range(8):
            dq.add_last(i)

        for _ in range(4):
            dq.remove_first()

        for i in range(8, 12):
            dq.add_last(i)

        assert contents(dq) == [4, 5, 6, 7, 8, 9, 10, 11]


class TestIndexOperations:
    def test_add_front(self):
        dq = BoundedDeque(b=5)

        dq.add(0, 1)
        dq.add(0, 0)

        assert contents(dq) == [0, 1]

    def test_add_back(self):
        dq = BoundedDeque(b=5)

        dq.add(0, 1)
        dq.add(1, 2)

        assert contents(dq) == [1, 2]

    def test_add_middle(self):
        dq = BoundedDeque(b=8)

        dq.add_last(1)
        dq.add_last(3)

        dq.add(1, 2)

        assert contents(dq) == [1, 2, 3]

    def test_remove_middle(self):
        dq = BoundedDeque(b=8)

        for i in [1, 2, 3, 4]:
            dq.add_last(i)

        assert dq.remove(1) == 2
        assert contents(dq) == [1, 3, 4]

    def test_get_matches_contents(self):
        dq = BoundedDeque(b=8)

        for i in range(6):
            dq.add_last(i)

        for i in range(6):
            assert dq.get(i) == i


class TestDequeFacade:
    def test_fifo_behavior(self):
        dq = BoundedDeque(b=10)

        for i in range(10):
            dq.add_last(i)

        out = [dq.remove_first() for _ in range(10)]

        assert out == list(range(10))

    def test_reverse_fifo_behavior(self):
        dq = BoundedDeque(b=10)

        for i in range(10):
            dq.add_first(i)

        out = [dq.remove_last() for _ in range(10)]

        assert out == list(range(10))

    def test_lifo_front_behavior(self):
        dq = BoundedDeque(b=10)

        for i in range(10):
            dq.add_first(i)

        out = [dq.remove_first() for _ in range(10)]

        assert out == list(reversed(range(10)))

    def test_lifo_back_behavior(self):
        dq = BoundedDeque(b=10)

        for i in range(10):
            dq.add_last(i)

        out = [dq.remove_last() for _ in range(10)]

        assert out == list(reversed(range(10)))


class TestStress:
    def test_fill_empty_fill_again(self):
        dq = BoundedDeque(b=16)

        for _ in range(3):
            for i in range(dq.capacity):
                dq.add_last(i)

            assert dq.size == dq.capacity

            while not dq.is_empty():
                dq.remove_first()

            assert dq.size == 0

    def test_many_wraparound_cycles(self):
        dq = BoundedDeque(b=16)

        for i in range(16):
            dq.add_last(i)

        for _ in range(100):
            x = dq.remove_first()
            dq.add_last(x)

        assert sorted(contents(dq)) == list(range(16))
