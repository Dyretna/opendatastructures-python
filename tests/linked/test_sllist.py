import pytest

from ods.linked import SLList


@pytest.fixture
def empty():
    return SLList()


@pytest.fixture
def single():
    return SLList([1])


@pytest.fixture
def three():
    return SLList([1, 2, 3])


@pytest.fixture
def five():
    return SLList([1, 2, 3, 4, 5])


class TestConstructor:
    def test_init_without_args_gives_empty(self, empty):
        assert empty.size == 0
        assert empty.head is None
        assert empty.tail is None

    @pytest.mark.parametrize(
        "source,expected",
        [
            ([], []),
            ((1,), [1]),
            ([1, 2, 3], [1, 2, 3]),
            ("ab", ["a", "b"]),
            (range(3), [0, 1, 2]),
        ],
    )
    def test_init_from_iterables(self, source, expected):
        s = SLList(source)
        assert s.to_list() == expected
        assert s.size == len(expected)

    def test_init_from_generator(self):
        s = SLList(x * 2 for x in range(3))
        assert s.to_list() == [0, 2, 4]
        assert s.size == 3

    def test_init_sets_head_and_tail(self, three):
        assert three.head.x == 1
        assert three.tail.x == 3
        assert three.tail.next is None


class TestAddAll:
    def test_add_all_into_empty(self, empty):
        empty.add_all(0, [10, 20])
        assert empty.to_list() == [10, 20]

    def test_add_all_at_front(self, three):
        three.add_all(0, [-2, -1])
        assert three.to_list() == [-2, -1, 1, 2, 3]

    @pytest.mark.parametrize(
        "i,expected",
        [
            (0, [7, 8, 1, 2, 3]),
            (1, [1, 7, 8, 2, 3]),
            (2, [1, 2, 7, 8, 3]),
            (3, [1, 2, 3, 7, 8]),
        ],
    )
    def test_add_all_at_all_positions(self, three, i, expected):
        three.add_all(i, [7, 8])
        assert three.to_list() == expected
        assert three.size == 5

    def test_add_all_empty_iterable_is_noop(self, three):
        three.add_all(1, [])
        assert three.to_list() == [1, 2, 3]
        assert three.size == 3

    def test_add_all_invalid_index_raises(self, three):
        with pytest.raises(IndexError):
            three.add_all(4, [7])

    def test_add_all_keeps_tail(self, three):
        three.add_all(3, [4, 5])
        assert three.tail.x == 5
        assert three.tail.next is None


class TestDelegation:
    def test_push_equals_add_first_equals_add_0(self, empty):
        assert empty.push("a") == "a"

        s = SLList()
        assert s.add_first("a") == "a"

        t = SLList()
        assert t.add(0, "a") == "a"

        assert s.to_list() == t.to_list()

    def test_add_last_equals_add_n(self, three):
        r1 = SLList([1, 2, 3])
        r1.add_last(4)
        r2 = SLList([1, 2, 3])
        r2.add(3, 4)
        assert r1.to_list() == r2.to_list() == [1, 2, 3, 4]

    def test_pop_equals_remove_first_equals_remove_0(self, three):
        r1 = SLList([1, 2, 3])
        r2 = SLList([1, 2, 3])
        r3 = SLList([1, 2, 3])

        assert r1.pop() == r2.remove_first() == r3.remove(0)

    def test_remove_last_equals_remove_n_minus_1(self, five):
        assert five.remove_last() == 5

        g = SLList([1, 2, 3, 4, 5])
        assert g.remove(g.size - 1) == 5
        assert five.to_list() == g.to_list() == [1, 2, 3, 4]

    def test_all_remove_facade_return_x(self, three):
        assert three.remove_first() == 1
        assert three.remove_last() == 3
        assert three.pop() == 2
        assert three.size == 0


class TestStack:
    def test_push_on_empty_sets_head_and_tail(self, empty):
        empty.push("a")
        assert empty.head is empty.tail
        assert empty.head.x == "a"

    @pytest.mark.parametrize("values", [[1], [1, 2], [7, 8, 9, 10]])
    def test_pop_lifo_order(self, values):
        s = SLList()
        for v in values:
            s.push(v)
        popped = [s.pop() for _ in values]
        assert popped == list(reversed(values))

    def test_pop_single_empties_list(self, single):
        assert single.pop() == 1
        assert single.head is None
        assert single.tail is None

    def test_pop_empty_returns_none(self, empty):
        assert empty.pop() is None


class TestQueue:
    def test_add_last_on_empty_sets_head_and_tail(self, empty):
        empty.add_last(9)
        assert empty.head is empty.tail

    def test_fifo_order(self, empty):
        for v in (1, 2, 3):
            empty.add_last(v)
        assert [empty.remove_first() for _ in range(3)] == [1, 2, 3]
        assert empty.head is None and empty.tail is None


class TestGetSet:
    @pytest.mark.parametrize("i,expected", [(0, 1), (1, 2), (2, 3)])
    def test_get_valid_indices(self, three, i, expected):
        assert three.get(i) == expected

    @pytest.mark.parametrize("i", [-1, 3, 10])
    def test_get_invalid_indices_raise(self, three, i):
        with pytest.raises(IndexError):
            three.get(i)

    def test_set_updates_value(self, three):
        three.set(1, "x")
        assert three.to_list() == [1, "x", 3]

    @pytest.mark.parametrize("i", [-1, 3])
    def test_set_invalid_indices_raise(self, three, i):
        with pytest.raises(IndexError):
            three.set(i, "x")


class TestAddRemoveGeneral:
    @pytest.mark.parametrize(
        "i,expected",
        [
            (0, [9, 1, 2, 3]),
            (1, [1, 9, 2, 3]),
            (2, [1, 2, 9, 3]),
            (3, [1, 2, 3, 9]),
        ],
    )
    def test_add_middle_and_edges(self, three, i, expected):
        three.add(i, 9)
        assert three.to_list() == expected

    @pytest.mark.parametrize(
        "i,removed,rest",
        [
            (0, 1, [2, 3]),
            (1, 2, [1, 3]),
            (2, 3, [1, 2]),
        ],
    )
    def test_remove_all_positions(self, three, i, removed, rest):
        assert three.remove(i) == removed
        assert three.to_list() == rest
        assert three.size == 2

    def test_add_beyond_end_raises(self, three):
        with pytest.raises(IndexError):
            three.add(4, "x")

    def test_remove_empty_returns_none(self, empty):
        assert empty.remove(0) is None

    def test_remove_last_empty_returns_none(self, empty):
        assert empty.remove_last() is None

    def test_repeated_removes_leave_consistent_state(self, five):
        for _ in range(5):
            five.remove(0)
        assert five.size == 0
        assert five.head is None
        assert five.tail is None
        five.add_last(1)
        assert five.to_list() == [1]
        assert five.tail.x == 1


class TestCheckSize:
    @pytest.mark.parametrize("values", [[], [1], [1, 2, 3], [1, 2, 3, 4, 5]])
    def test_check_size_passes_on_consistent_lists(self, values):
        s = SLList(values)
        s.check_size()

    def test_check_size_detects_corrupted_n(self, three):
        three.n = 10
        with pytest.raises(AssertionError):
            three.check_size()


class TestUtilities:
    def test_reverse(self, three):
        three.reverse()
        assert three.to_list() == [3, 2, 1]
        assert three.head.x == 3
        assert three.tail.x == 1
        three.check_size()

    def test_reverse_twice_restores(self, five):
        five.reverse()
        five.reverse()
        assert five.to_list() == [1, 2, 3, 4, 5]

    def test_reverse_empty_and_single(self, empty, single):
        empty.reverse()
        assert empty.head is None
        single.reverse()
        assert single.head is single.tail

    @pytest.mark.parametrize(
        "values,expected",
        [
            ([], None),
            ([7], None),
            ([1, 2], 1),
            ([1, 2, 3], 2),
            ([1, 2, 3, 4], 3),
        ],
    )
    def test_second_last(self, values, expected):
        assert SLList(values).second_last() == expected


class TestIteration:
    def test_iter_yields_original_values(self, three):
        assert list(three) == [1, 2, 3]
        assert all(type(x) is int for x in three)

    def test_iter_does_not_mutate_original(self, three):
        list(three)
        assert three.size == 3
        assert three.head.x == 1
        assert three.tail.x == 3
        three.check_size()

    def test_to_list_matches_iter(self, five):
        assert five.to_list() == list(five)

    def test_size_tracks_mixed_operations(self):
        s = SLList([1, 2])
        s.push(0)
        s.add_last(3)
        assert s.size == 4
        s.pop()
        s.remove_last()
        assert s.size == 2
        assert s.to_list() == [1, 2]
