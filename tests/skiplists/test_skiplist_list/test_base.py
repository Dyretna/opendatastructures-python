import pytest

from ods.skip_list.skiplist_list import SkiplistList


@pytest.fixture
def sl():
    return SkiplistList()


@pytest.fixture
def flat_heights(monkeypatch):
    """Force all node heights to 0 for deterministic structure tests."""
    monkeypatch.setattr(SkiplistList, "_pick_height", lambda self: 0)


class TestSkiplistListConstruction:
    def test_new_list_is_empty(self, sl):
        assert len(sl) == 0
        assert sl.n == 0
        assert sl.h == 0
        assert sl.to_list() == []

    def test_sentinel_initial_state(self, sl):
        assert sl.sentinel.x is None
        assert sl.sentinel.height == 0
        assert sl.sentinel.next == [None]
        assert sl.sentinel.length == [0]


class TestAdd:
    @pytest.mark.parametrize(
        "values",
        [
            [1],
            [1, 2],
            [1, 2, 3],
            [10, 20, 30, 40, 50],
        ],
    )
    def test_add_at_end(self, sl, values, monkeypatch):
        # set all nodes to height 0
        # to make deterministic tests
        monkeypatch.setattr(SkiplistList, "_pick_height", lambda self: 0)

        for i, value in enumerate(values):
            sl.add(i, value)

        assert sl.to_list() == values
        assert len(sl) == len(values)

    @pytest.mark.parametrize(
        "values,expected",
        [
            ([1, 2, 3], [99, 1, 2, 3]),
            ([10, 20], [99, 10, 20]),
            ([7], [99, 7]),
        ],
    )
    def test_add_at_front(self, sl, values, expected):
        for i, value in enumerate(values):
            sl.add(i, value)

        sl.add(0, 99)

        assert sl.to_list() == expected

    @pytest.mark.parametrize(
        "index,value,expected",
        [
            (1, 99, [1, 99, 2, 3]),
            (2, 99, [1, 2, 99, 3]),
            (3, 99, [1, 2, 3, 99]),
        ],
    )
    def test_add_at_arbitrary_position(self, sl, index, value, expected):
        for i, x in enumerate([1, 2, 3]):
            sl.add(i, x)

        sl.add(index, value)
        assert sl.to_list() == expected


class TestRemove:
    @pytest.mark.parametrize(
        "remove_index,expected_removed,expected_list",
        [
            (0, 10, [20, 30, 40]),
            (1, 20, [10, 30, 40]),
            (2, 30, [10, 20, 40]),
            (3, 40, [10, 20, 30]),
        ],
    )
    def test_remove(self, sl, remove_index, expected_removed, expected_list):
        for i, x in enumerate([10, 20, 30, 40]):
            sl.add(i, x)

        removed = sl.remove(remove_index)

        assert removed == expected_removed
        assert sl.to_list() == expected_list
        assert len(sl) == len(expected_list)


class TestInternalInvariants:
    def test_n_matches_number_of_items(self, sl):
        for i in range(10):
            sl.add(i, i)

        assert sl.n == len(sl.to_list())

    def test_height_never_exceeds_sentinel_height(self, sl):
        for i in range(100):
            sl.add(i, i)

        assert sl.h <= sl.sentinel.height

    def test_sentinel_arrays_have_same_length(self, sl):
        for i in range(100):
            sl.add(i, i)

        assert len(sl.sentinel.next) == len(sl.sentinel.length)
