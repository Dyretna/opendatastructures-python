import pytest

from ods.skip_list.skiplist_list import SkiplistList


class TestSkiplistListConstruction:
    def test_new_list_is_empty(self):
        sl = SkiplistList()

        assert len(sl) == 0
        assert sl.n == 0
        assert sl.h == 0
        assert sl.to_list() == []

    def test_sentinel_initial_state(self):
        sl = SkiplistList()

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
    def test_add_at_end(self, values, monkeypatch):
        # set all nodes to height 0
        # to make deterministic tests
        monkeypatch.setattr(SkiplistList, "_pick_height", lambda self: 0)

        sl = SkiplistList()

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
    def test_add_at_front(self, values, expected):
        sl = SkiplistList()

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
    def test_add_at_arbitrary_position(self, index, value, expected):
        sl = SkiplistList()

        for i, x in enumerate([1, 2, 3]):
            sl.add(i, x)

        sl.add(index, value)

        assert sl.to_list() == expected


class TestGet:
    @pytest.mark.parametrize(
        "index,expected",
        [
            (0, 10),
            (1, 20),
            (2, 30),
            (3, 40),
            (4, 50),
        ],
    )
    def test_get_returns_correct_value(self, index, expected):
        sl = SkiplistList()

        for i, x in enumerate([10, 20, 30, 40, 50]):
            sl.add(i, x)

        assert sl.get(index) == expected


class TestSet:
    @pytest.mark.parametrize(
        "index,new_value,old_value",
        [
            (0, 100, 10),
            (1, 200, 20),
            (2, 300, 30),
        ],
    )
    def test_set_returns_old_value(self, index, new_value, old_value):
        sl = SkiplistList()

        for i, x in enumerate([10, 20, 30]):
            sl.add(i, x)

        assert sl.set(index, new_value) == old_value

    @pytest.mark.parametrize(
        "index,new_value,expected",
        [
            (0, 100, [100, 20, 30]),
            (1, 200, [10, 200, 30]),
            (2, 300, [10, 20, 300]),
        ],
    )
    def test_set_updates_value(self, index, new_value, expected):
        sl = SkiplistList()

        for i, x in enumerate([10, 20, 30]):
            sl.add(i, x)

        sl.set(index, new_value)

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
    def test_remove(self, remove_index, expected_removed, expected_list):
        sl = SkiplistList()

        for i, x in enumerate([10, 20, 30, 40]):
            sl.add(i, x)

        removed = sl.remove(remove_index)

        assert removed == expected_removed
        assert sl.to_list() == expected_list
        assert len(sl) == len(expected_list)


class TestSequenceOperations:
    def test_add_get_set_remove_sequence(self):
        sl = SkiplistList()

        sl.add(0, 10)
        sl.add(1, 20)
        sl.add(2, 30)

        assert sl.to_list() == [10, 20, 30]

        assert sl.get(1) == 20

        old = sl.set(1, 99)

        assert old == 20
        assert sl.to_list() == [10, 99, 30]

        removed = sl.remove(1)

        assert removed == 99
        assert sl.to_list() == [10, 30]

    def test_matches_python_list_behavior(self):
        sl = SkiplistList()
        expected = []

        for value in [10, 20, 30, 40, 50]:
            sl.add(len(expected), value)
            expected.append(value)

        sl.add(2, 99)
        expected.insert(2, 99)

        sl.set(4, 111)
        expected[4] = 111

        assert sl.to_list() == expected


class TestInternalInvariants:
    def test_n_matches_number_of_items(self):
        sl = SkiplistList()

        for i in range(10):
            sl.add(i, i)

        assert sl.n == len(sl.to_list())

    def test_height_never_exceeds_sentinel_height(self):
        sl = SkiplistList()

        for i in range(100):
            sl.add(i, i)

        assert sl.h <= sl.sentinel.height

    def test_sentinel_arrays_have_same_length(self):
        sl = SkiplistList()

        for i in range(100):
            sl.add(i, i)

        assert len(sl.sentinel.next) == len(sl.sentinel.length)
