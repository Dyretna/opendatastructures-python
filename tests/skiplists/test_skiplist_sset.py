import random

import pytest

from ods.skip_list.skiplist_sset import SkiplistSSet


@pytest.fixture
def sl():
    return SkiplistSSet()


class TestConstruction:
    def test_new_skiplist_is_empty(self, sl):
        assert len(sl) == 0
        assert sl.to_list() == []
        assert sl.find(10) is None

    def test_add_single_element(self, sl):
        assert sl.add(5) is True

        assert len(sl) == 1
        assert sl.to_list() == [5]
        assert sl.find(5) == 5

    def test_add_keeps_sorted_order(self, sl):
        values = [5, 3, 7, 1, 9]

        for v in values:
            sl.add(v)

        assert sl.to_list() == [1, 3, 5, 7, 9]

    def test_add_duplicate_returns_false(self, sl):
        assert sl.add(5) is True
        assert sl.add(5) is False

        assert len(sl) == 1
        assert sl.to_list() == [5]


class TestFind:
    def test_find_existing_values(self, sl):
        for v in [1, 3, 5, 7, 9]:
            sl.add(v)

        assert sl.find(1) == 1
        assert sl.find(5) == 5
        assert sl.find(9) == 9

    def test_find_returns_successor(self, sl):
        for v in [1, 3, 5, 7, 9]:
            sl.add(v)

        assert sl.find(0) == 1
        assert sl.find(2) == 3
        assert sl.find(4) == 5
        assert sl.find(8) == 9

    def test_find_returns_none_when_no_successor(self, sl):
        for v in [1, 3, 5]:
            sl.add(v)

        assert sl.find(10) is None


class TestContains:
    def test_contains(self, sl):
        sl.add(42)

        assert 42 in sl
        assert 99 not in sl


class TestRemove:
    def test_remove_existing_element(self, sl):
        for v in [1, 3, 5, 7, 9]:
            sl.add(v)

        assert sl.remove(5) is True

        assert len(sl) == 4
        assert sl.to_list() == [1, 3, 7, 9]
        assert 5 not in sl

    def test_remove_first_element(self, sl):
        for v in [1, 3, 5]:
            sl.add(v)

        assert sl.remove(1) is True

        assert sl.to_list() == [3, 5]

    def test_remove_last_element(self, sl):
        for v in [1, 3, 5]:
            sl.add(v)

        assert sl.remove(5) is True

        assert sl.to_list() == [1, 3]

    def test_remove_non_existing_element(self, sl):
        for v in [1, 3, 5]:
            sl.add(v)

        assert sl.remove(10) is False

        assert len(sl) == 3
        assert sl.to_list() == [1, 3, 5]

    def test_remove_until_empty(self, sl):
        values = [1, 2, 3, 4, 5]

        for v in values:
            sl.add(v)

        for v in values:
            assert sl.remove(v) is True

        assert len(sl) == 0
        assert sl.to_list() == []


class TestRandomizedBehaviour:
    def test_random_insertions_match_python_set(self):
        sl = SkiplistSSet()
        reference = set()

        values = list(range(100))
        random.shuffle(values)

        for v in values:
            sl.add(v)
            reference.add(v)

        assert sl.to_list() == sorted(reference)
        assert len(sl) == len(reference)

    def test_random_insertions_and_removals(self):
        sl = SkiplistSSet()
        reference = set()

        values = list(range(100))

        for v in values:
            sl.add(v)
            reference.add(v)

        random.shuffle(values)

        for v in values[:50]:
            assert sl.remove(v) is True
            reference.remove(v)

        assert sl.to_list() == sorted(reference)
        assert len(sl) == len(reference)


class TestheightHandling:
    def test_height_growth_does_not_break_structure(self, monkeypatch):
        heights = iter([4, 3, 2, 1, 0])

        def fake_height():
            return next(heights)

        sl = SkiplistSSet()

        monkeypatch.setattr(sl, "_pick_height", fake_height)

        for v in [10, 20, 30, 40, 50]:
            sl.add(v)

        assert sl.to_list() == [10, 20, 30, 40, 50]
        assert len(sl) == 5


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
    def test_len_matches_number_of_elements(self, values):
        sl = SkiplistSSet()

        for v in values:
            sl.add(v)

        assert len(sl) == len(set(values))
