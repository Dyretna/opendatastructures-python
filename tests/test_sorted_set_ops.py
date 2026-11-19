"""
SortedSet contract tests.

Runs against every class registered in SORTED_SET_IMPLS
(tests/implementations.py), via the sorted_set_seq fixture in conftest.py.

Contract assumptions:

    * add(x) -> bool
    * remove(x) -> bool
    * find(x) returns x if present
    * find(x) returns the successor of x otherwise
    * find(x) returns None when no successor exists
    * duplicates are not stored
    * iteration order is sorted
"""

import random

import pytest


def contents(s):
    return s.to_list()


class TestConstruction:
    def test_new_set_is_empty(self, sorted_set_seq):
        assert sorted_set_seq.size == 0
        assert len(sorted_set_seq) == 0
        assert sorted_set_seq.is_empty()
        assert contents(sorted_set_seq) == []

    def test_add_single_element(self, sorted_set_seq):
        assert sorted_set_seq.add(5) is True

        assert sorted_set_seq.size == 1
        assert not sorted_set_seq.is_empty()
        assert contents(sorted_set_seq) == [5]

    def test_add_keeps_sorted_order(self, sorted_set_seq):
        for v in [5, 3, 7, 1, 9]:
            sorted_set_seq.add(v)

        assert contents(sorted_set_seq) == [1, 3, 5, 7, 9]

    def test_add_duplicate_returns_false(self, sorted_set_seq):
        assert sorted_set_seq.add(5) is True
        assert sorted_set_seq.add(5) is False

        assert sorted_set_seq.size == 1
        assert contents(sorted_set_seq) == [5]

    def test_duplicates_do_not_change_contents(self, sorted_set_seq):
        values = [5, 3, 5, 1, 3, 7, 1]

        for v in values:
            sorted_set_seq.add(v)

        assert contents(sorted_set_seq) == [1, 3, 5, 7]


class TestFind:
    def test_find_on_empty_returns_none(self, sorted_set_seq):
        assert sorted_set_seq.find(10) is None

    def test_find_existing_values(self, sorted_set_seq):
        for v in [1, 3, 5, 7, 9]:
            sorted_set_seq.add(v)

        assert sorted_set_seq.find(1) == 1
        assert sorted_set_seq.find(5) == 5
        assert sorted_set_seq.find(9) == 9

    def test_find_returns_successor(self, sorted_set_seq):
        for v in [1, 3, 5, 7, 9]:
            sorted_set_seq.add(v)

        assert sorted_set_seq.find(0) == 1
        assert sorted_set_seq.find(2) == 3
        assert sorted_set_seq.find(4) == 5
        assert sorted_set_seq.find(8) == 9

    def test_find_returns_none_when_no_successor_exists(self, sorted_set_seq):
        for v in [1, 3, 5]:
            sorted_set_seq.add(v)

        assert sorted_set_seq.find(10) is None

    def test_find_smallest_successor(self, sorted_set_seq):
        for v in [10, 20, 30, 40]:
            sorted_set_seq.add(v)

        assert sorted_set_seq.find(11) == 20
        assert sorted_set_seq.find(21) == 30
        assert sorted_set_seq.find(31) == 40


class TestContains:
    def test_contains_existing(self, sorted_set_seq):
        sorted_set_seq.add(42)

        assert 42 in sorted_set_seq

    def test_contains_missing(self, sorted_set_seq):
        sorted_set_seq.add(42)

        assert 99 not in sorted_set_seq


class TestRemove:
    def test_remove_existing_value(self, sorted_set_seq):
        for v in [1, 3, 5, 7, 9]:
            sorted_set_seq.add(v)

        assert sorted_set_seq.remove(5) is True

        assert contents(sorted_set_seq) == [1, 3, 7, 9]
        assert 5 not in sorted_set_seq

    def test_remove_missing_value_returns_false(self, sorted_set_seq):
        for v in [1, 3, 5]:
            sorted_set_seq.add(v)

        assert sorted_set_seq.remove(10) is False

        assert contents(sorted_set_seq) == [1, 3, 5]

    def test_remove_smallest_value(self, sorted_set_seq):
        for v in [1, 3, 5]:
            sorted_set_seq.add(v)

        assert sorted_set_seq.remove(1) is True

        assert contents(sorted_set_seq) == [3, 5]

    def test_remove_largest_value(self, sorted_set_seq):
        for v in [1, 3, 5]:
            sorted_set_seq.add(v)

        assert sorted_set_seq.remove(5) is True

        assert contents(sorted_set_seq) == [1, 3]

    def test_remove_until_empty(self, sorted_set_seq):
        for v in [1, 2, 3, 4, 5]:
            sorted_set_seq.add(v)

        for v in [1, 2, 3, 4, 5]:
            assert sorted_set_seq.remove(v) is True

        assert sorted_set_seq.size == 0
        assert sorted_set_seq.is_empty()
        assert contents(sorted_set_seq) == []

    def test_remove_same_value_twice(self, sorted_set_seq):
        sorted_set_seq.add(10)

        assert sorted_set_seq.remove(10) is True
        assert sorted_set_seq.remove(10) is False


class TestSize:
    @pytest.mark.parametrize(
        "values",
        [
            [],
            [1],
            [1, 2],
            [5, 3, 7, 1, 9],
            list(range(20)),
        ],
    )
    def test_size_matches_unique_elements(self, sorted_set_seq, values):
        for v in values:
            sorted_set_seq.add(v)

        assert sorted_set_seq.size == len(set(values))

    def test_duplicate_add_does_not_change_size(self, sorted_set_seq):
        sorted_set_seq.add(123)

        before = sorted_set_seq.size

        sorted_set_seq.add(123)

        assert sorted_set_seq.size == before


class TestMixedOps:
    def test_add_remove_add(self, sorted_set_seq):
        sorted_set_seq.add(10)
        sorted_set_seq.add(20)

        sorted_set_seq.remove(10)

        sorted_set_seq.add(15)

        assert contents(sorted_set_seq) == [15, 20]

    def test_find_after_removal(self, sorted_set_seq):
        for v in [10, 20, 30]:
            sorted_set_seq.add(v)

        sorted_set_seq.remove(20)

        assert sorted_set_seq.find(20) == 30

    def test_repeated_add_remove_cycles(self, sorted_set_seq):
        for _ in range(5):
            for i in range(100):
                assert sorted_set_seq.add(i) is True

            assert sorted_set_seq.size == 100

            for i in range(100):
                assert sorted_set_seq.remove(i) is True

            assert sorted_set_seq.size == 0
            assert sorted_set_seq.is_empty()


class TestRandomizedBehaviour:
    def test_random_insertions_match_python_set(self, sorted_set_seq):
        reference = set()

        values = list(range(100))
        random.shuffle(values)

        for v in values:
            sorted_set_seq.add(v)
            reference.add(v)

        assert contents(sorted_set_seq) == sorted(reference)
        assert sorted_set_seq.size == len(reference)

    def test_random_insertions_and_removals_match_python_set(self, sorted_set_seq):
        reference = set()

        values = list(range(100))

        for v in values:
            sorted_set_seq.add(v)
            reference.add(v)

        random.shuffle(values)

        for v in values[:50]:
            assert sorted_set_seq.remove(v) is True
            reference.remove(v)

        assert contents(sorted_set_seq) == sorted(reference)
        assert sorted_set_seq.size == len(reference)

    def test_random_operations_match_reference_model(self, sorted_set_seq):
        rng = random.Random(20261119)
        reference = set()

        for _ in range(1000):
            value = rng.randint(0, 100)
            op = rng.random()

            if op < 0.50:
                expected = value not in reference

                assert sorted_set_seq.add(value) is expected

                reference.add(value)

            elif op < 0.75:
                expected = value in reference

                assert sorted_set_seq.remove(value) is expected

                reference.discard(value)

            else:
                expected = min(
                    (x for x in reference if x >= value),
                    default=None,
                )

                assert sorted_set_seq.find(value) == expected

        assert contents(sorted_set_seq) == sorted(reference)
        assert sorted_set_seq.size == len(reference)
