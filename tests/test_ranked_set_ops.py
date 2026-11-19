"""
RankedSortedSet contract tests.

Runs against every class registered in RANKED_SET_IMPLS
(tests/implementations.py), via the ranked_set fixture in conftest.py.

Additional contract beyond SortedSet:

    * get(i) returns the i:th smallest element
    * rank access reflects sorted order
    * mutations preserve rank semantics
"""

import random

import pytest


def sorted_contents(s):
    return s.to_list()


class TestGet:
    def test_get_single_element(self, ranked_set_seq):
        ranked_set_seq.add(7)

        assert ranked_set_seq.get(0) == 7

    def test_get_returns_sorted_order(self, ranked_set_seq):
        for v in [5, 3, 7, 1, 9]:
            ranked_set_seq.add(v)

        assert ranked_set_seq.get(0) == 1
        assert ranked_set_seq.get(1) == 3
        assert ranked_set_seq.get(2) == 5
        assert ranked_set_seq.get(3) == 7
        assert ranked_set_seq.get(4) == 9

    def test_get_all_positions(self, ranked_set_seq):
        values = [9, 1, 5, 7, 3]

        for v in values:
            ranked_set_seq.add(v)

        expected = sorted(values)

        for i, x in enumerate(expected):
            assert ranked_set_seq.get(i) == x

    def test_get_after_duplicate_adds(self, ranked_set_seq):
        for v in [5, 3, 5, 1, 3, 7]:
            ranked_set_seq.add(v)

        expected = [1, 3, 5, 7]

        for i, x in enumerate(expected):
            assert ranked_set_seq.get(i) == x

    @pytest.mark.parametrize("bad_index", [-1, 5])
    def test_get_out_of_bounds_raises(self, ranked_set_seq, bad_index):
        for v in [1, 2, 3, 4, 5]:
            ranked_set_seq.add(v)

        with pytest.raises(IndexError):
            ranked_set_seq.get(bad_index)


class TestGetAfterMutations:
    def test_get_after_removal(self, ranked_set_seq):
        for v in [1, 3, 5, 7, 9]:
            ranked_set_seq.add(v)

        ranked_set_seq.remove(5)

        expected = [1, 3, 7, 9]

        for i, x in enumerate(expected):
            assert ranked_set_seq.get(i) == x

    def test_get_after_removing_smallest(self, ranked_set_seq):
        for v in [1, 2, 3, 4, 5]:
            ranked_set_seq.add(v)

        ranked_set_seq.remove(1)

        expected = [2, 3, 4, 5]

        for i, x in enumerate(expected):
            assert ranked_set_seq.get(i) == x

    def test_get_after_removing_largest(self, ranked_set_seq):
        for v in [1, 2, 3, 4, 5]:
            ranked_set_seq.add(v)

        ranked_set_seq.remove(5)

        expected = [1, 2, 3, 4]

        for i, x in enumerate(expected):
            assert ranked_set_seq.get(i) == x

    def test_get_after_add_remove_add(self, ranked_set_seq):
        ranked_set_seq.add(10)
        ranked_set_seq.add(30)

        ranked_set_seq.remove(30)
        ranked_set_seq.add(20)

        assert ranked_set_seq.get(0) == 10
        assert ranked_set_seq.get(1) == 20


class TestConsistency:
    def test_get_matches_to_list(self, ranked_set_seq):
        for v in [5, 1, 8, 3]:
            ranked_set_seq.add(v)

        expected = sorted_contents(ranked_set_seq)

        for i, x in enumerate(expected):
            assert ranked_set_seq.get(i) == x

    def test_every_rank_accessible(self, ranked_set_seq):
        values = list(range(100))

        for v in values:
            ranked_set_seq.add(v)

        for i in range(100):
            assert ranked_set_seq.get(i) == i


class TestRandomizedBehaviour:
    def test_random_get_matches_sorted_reference(self, ranked_set_seq):
        reference = set()

        values = list(range(100))
        random.shuffle(values)

        for v in values:
            ranked_set_seq.add(v)
            reference.add(v)

        expected = sorted(reference)

        for i, x in enumerate(expected):
            assert ranked_set_seq.get(i) == x

    def test_random_operations_preserve_rank_order(self, ranked_set_seq):
        rng = random.Random(20261119)
        reference = set()

        for _ in range(1000):
            value = rng.randint(0, 100)

            if rng.random() < 0.6:
                ranked_set_seq.add(value)
                reference.add(value)
            else:
                ranked_set_seq.remove(value)
                reference.discard(value)

        expected = sorted(reference)

        assert ranked_set_seq.size == len(expected)

        for i, x in enumerate(expected):
            assert ranked_set_seq.get(i) == x

    def test_random_mixed_operations_match_reference_model(self, ranked_set_seq):
        rng = random.Random(7)
        reference = set()

        for _ in range(500):
            value = rng.randint(0, 100)

            if not reference or rng.random() < 0.6:
                ranked_set_seq.add(value)
                reference.add(value)
            else:
                ranked_set_seq.remove(value)
                reference.discard(value)

            expected = sorted(reference)

            assert ranked_set_seq.size == len(expected)

            for i, x in enumerate(expected):
                assert ranked_set_seq.get(i) == x
