"""Implementation-specific tests for MinQueue.

Internals and extras unique to MinQueue. The add/remove
contract is covered by tests/test_queue_ops.py (QUEUE_IMPLS) and the
invariants by test_invariants.py (seq).
"""

import pytest

from ods.arrays import MinQueue


@pytest.fixture
def min_queue():
    return MinQueue()


class TestFifoSemantics:
    def test_remove_returns_first_added(self, min_queue):
        min_queue.add(10)
        min_queue.add(20)
        min_queue.add(30)
        assert min_queue.remove() == 10
        assert min_queue.size == 2

    def test_fifo_drains_in_insertion_order(self, min_queue):
        values = [10, 20, 30, 40]
        for v in values:
            min_queue.add(v)
        drained = [min_queue.remove() for _ in range(min_queue.size)]
        assert drained == values

    def test_remove_from_empty_raises(self, min_queue):
        assert min_queue.is_empty()
        with pytest.raises(IndexError):
            min_queue.remove()

    def test_remove_from_empty_after_drain_raises(self, min_queue):
        for v in [1, 2]:
            min_queue.add(v)
        min_queue.remove()
        min_queue.remove()
        with pytest.raises(IndexError):
            min_queue.remove()


class TestRunningMinimum:
    def test_get_min_single_element(self, min_queue):
        min_queue.add(42)
        assert min_queue.get_min() == 42

    def test_get_min_tracks_running_minimum(self, min_queue):
        for v in [5, 3, 8, 1, 7]:
            min_queue.add(v)
        assert min_queue.get_min() == 1

    def test_min_updated_after_removing_minimum(self, min_queue):
        for v in [5, 3, 8, 1, 7]:
            min_queue.add(v)

        min_queue.remove()  # 5 — min unchanged
        assert min_queue.get_min() == 1

        min_queue.remove()  # 3 — min unchanged
        assert min_queue.get_min() == 1

        min_queue.remove()  # 8 — min unchanged
        assert min_queue.get_min() == 1

        min_queue.remove()  # 1 — min must move to 7
        assert min_queue.get_min() == 7

    def test_min_with_duplicate_minima_across_transfer(self, min_queue):
        for v in [3, 1, 3, 1]:
            min_queue.add(v)
        assert min_queue.get_min() == 1

        min_queue.remove()  # 3
        assert min_queue.get_min() == 1
        min_queue.remove()  # 1 — second 1 still present
        assert min_queue.get_min() == 1

    def test_get_min_on_empty_raises(self, min_queue):
        with pytest.raises(IndexError):
            min_queue.get_min()

    def test_get_min_after_full_drain_and_refill(self, min_queue):
        min_queue.add(1)
        min_queue.remove()
        min_queue.add(10)
        assert min_queue.get_min() == 10


class TestTransferBehaviour:
    def test_transfer_preserves_fifo_and_min(self, min_queue):
        """Interleaved adds/removes force several out_stack rebuilds."""
        values = list(range(20))
        for v in values:
            min_queue.add(v)

        for expected in values:
            assert min_queue.get_min() == expected
            assert min_queue.remove() == expected

    def test_interleaved_add_remove_matches_reference(self, min_queue):
        ref = []
        for v in range(50):
            min_queue.add(v)
            ref.append(v)
            if v % 3 == 0 and ref:
                assert min_queue.remove() == ref.pop(0)

        while ref:
            assert min_queue.get_min() == min(ref)
            assert min_queue.remove() == ref.pop(0)

        assert min_queue.is_empty()

    def test_min_correct_when_queue_empty_between_transfers(self, min_queue):
        min_queue.add(7)
        assert min_queue.remove() == 7
        assert min_queue.is_empty()

        min_queue.add(2)
        assert min_queue.get_min() == 2


class TestIteration:
    def test_iteration_is_front_to_back(self, min_queue):
        for v in [10, 20, 30]:
            min_queue.add(v)
        assert list(min_queue) == [10, 20, 30]

    def test_iteration_does_not_mutate(self, min_queue):
        for v in [1, 2, 3]:
            min_queue.add(v)
        list(min_queue)
        assert min_queue.size == 3
        assert min_queue.get_min() == 1

    def test_iteration_across_pending_in_stack(self, min_queue):
        """Elements not yet transferred must also appear, in order."""
        for v in [1, 2, 3]:
            min_queue.add(v)
        min_queue.remove()  # forces transfer of everything
        min_queue.add(4)
        min_queue.add(5)
        assert list(min_queue) == [2, 3, 4, 5]
