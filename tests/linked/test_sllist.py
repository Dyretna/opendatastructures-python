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

    def test_init_sets_head_and_tail(self, three):
        assert three.head.x == 1
        assert three.tail.x == 3
        assert three.tail.next is None


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

    def test_size_tracks_mixed_operations(self):
        s = SLList([1, 2])
        s.push(0)
        s.add_last(3)
        assert s.size == 4
        s.pop()
        s.remove_last()
        assert s.size == 2
        assert s.to_list() == [1, 2]


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
