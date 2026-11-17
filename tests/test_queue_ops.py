"""Queue-contract tests: add(x) / remove() (FIFO).

Runs against every class registered in QUEUE_IMPLS
(tests/implementations.py), via the `queue_seq` fixture in conftest.py.

Covered elsewhere:
  * size/is_empty invariants -> test_invariants.py (seq)
  * min()-accessors and other extras -> per-implementation modules
"""

import random

import pytest
from helpers import drain_queue


class TestAddRemove:
    def test_add_increments_size(self, queue_seq):
        queue_seq.add(1)
        assert queue_seq.size == 1

    def test_remove_returns_first_added(self, queue_seq):
        queue_seq.add(10)
        queue_seq.add(20)
        queue_seq.add(30)
        assert queue_seq.remove() == 10
        assert queue_seq.size == 2

    def test_fifo_drains_in_insertion_order(self, queue_seq):
        values = [10, 20, 30, 40, 50]
        for v in values:
            queue_seq.add(v)
        assert drain_queue(queue_seq) == values

    def test_add_remove_single_element_repeatedly(self, queue_seq):
        for _ in range(10):
            queue_seq.add(1)
            assert queue_seq.remove() == 1
            assert queue_seq.is_empty()


class TestEdgeCases:
    def test_remove_from_empty_raises(self, queue_seq):
        assert queue_seq.is_empty()
        with pytest.raises(IndexError):
            queue_seq.remove()

    def test_alternating_with_empties(self, queue_seq):
        queue_seq.add(1)
        assert queue_seq.remove() == 1
        queue_seq.add(2)
        assert queue_seq.remove() == 2
        assert queue_seq.is_empty()


class TestGrowthShrinkage:
    def test_growth_after_many_adds(self, queue_seq):
        for i in range(1000):
            queue_seq.add(i)
        assert queue_seq.size == 1000

    def test_shrink_after_many_removes(self, queue_seq):
        for i in range(1000):
            queue_seq.add(i)
        for expected in range(1000):
            assert queue_seq.remove() == expected
        assert queue_seq.is_empty()

    def test_repeated_grow_and_shrink_cycles(self, queue_seq):
        for _ in range(5):
            for i in range(100):
                queue_seq.add(i)
            assert queue_seq.size == 100
            for _ in range(100):
                queue_seq.remove()
            assert queue_seq.is_empty()


class TestRandomizedStress:
    def test_matches_reference_queue(self, queue_seq):
        rng = random.Random(1717)
        ref = []

        for _ in range(500):
            if not ref or rng.random() < 0.55:
                v = rng.randint(0, 999)
                queue_seq.add(v)
                ref.append(v)
            else:
                assert queue_seq.remove() == ref.pop(0)

            assert queue_seq.size == len(ref)

        assert drain_queue(queue_seq) == ref
