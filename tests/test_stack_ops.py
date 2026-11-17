"""Stack-contract tests: push(x) / pop() (LIFO).

Runs against every class registered in STACK_IMPLS
(tests/implementations.py), via the `stack_seq` fixture in conftest.py.

Contract (base.py policies):
  * push(x) -> None
  * pop()   -> x (the popped value); IndexError on empty structure

Covered elsewhere:
  * size/is_empty invariants -> test_invariants.py (seq)
  * indexed list operations  -> test_index_ops.py (ArrayStack only)
  * min()-accessors and other extras -> per-implementation modules
"""

import random

import pytest
from helpers import drain_stack


class TestPushPop:
    def test_push_increments_size(self, stack_seq):
        stack_seq.push(1)
        assert stack_seq.size == 1

    def test_pop_returns_last_pushed(self, stack_seq):
        stack_seq.push(10)
        stack_seq.push(20)
        stack_seq.push(30)
        assert stack_seq.pop() == 30
        assert stack_seq.size == 2

    def test_lifo_drains_in_reverse(self, stack_seq):
        values = [10, 20, 30, 40, 50]
        for v in values:
            stack_seq.push(v)
        assert drain_stack(stack_seq) == list(reversed(values))

    def test_push_pop_single_element_repeatedly(self, stack_seq):
        for _ in range(10):
            stack_seq.push(1)
            assert stack_seq.pop() == 1
            assert stack_seq.is_empty()


class TestEdgeCases:
    def test_pop_from_empty_raises(self, stack_seq):
        assert stack_seq.is_empty()
        with pytest.raises(IndexError):
            stack_seq.pop()

    def test_alternating_with_empties(self, stack_seq):
        stack_seq.push(1)
        assert stack_seq.pop() == 1
        stack_seq.push(2)
        assert stack_seq.pop() == 2
        assert stack_seq.is_empty()


class TestGrowthShrinkage:
    def test_growth_after_many_pushes(self, stack_seq):
        for i in range(1000):
            stack_seq.push(i)
        assert stack_seq.size == 1000

    def test_shrink_after_many_pops(self, stack_seq):
        for i in range(1000):
            stack_seq.push(i)
        for expected in reversed(range(1000)):
            assert stack_seq.pop() == expected
        assert stack_seq.is_empty()

    def test_repeated_grow_and_shrink_cycles(self, stack_seq):
        for _ in range(5):
            for i in range(100):
                stack_seq.push(i)
            assert stack_seq.size == 100
            for _ in range(100):
                stack_seq.pop()
            assert stack_seq.is_empty()


class TestRandomizedStress:
    def test_matches_reference_stack(self, stack_seq):
        rng = random.Random(4242)
        ref = []

        for _ in range(500):
            if not ref or rng.random() < 0.55:
                v = rng.randint(0, 999)
                stack_seq.push(v)
                ref.append(v)
            else:
                assert stack_seq.pop() == ref.pop()

            assert stack_seq.size == len(ref)

        assert drain_stack(stack_seq) == list(reversed(ref))
