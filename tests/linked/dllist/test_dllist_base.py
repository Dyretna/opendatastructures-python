import pytest

from ods.linked import DLList


@pytest.fixture
def empty():
    return DLList()


@pytest.fixture
def single():
    return DLList([1])


@pytest.fixture
def three():
    return DLList([1, 2, 3])


@pytest.fixture
def five():
    return DLList([1, 2, 3, 4, 5])


class TestConstructor:
    def test_init_without_args_creates_empty_cycle(self, empty):
        assert empty.size == 0
        assert empty.dummy.next is empty.dummy
        assert empty.dummy.prev is empty.dummy

    @pytest.mark.parametrize(
        "source",
        [
            [],
            [1],
            [1, 2, 3],
            tuple(range(5)),
            range(4),
        ],
    )
    def test_init_from_iterable(self, source):
        dll = DLList(source)

        assert dll.to_list() == list(source)
        assert dll.size == len(list(source))

    def test_single_element_links_to_dummy(self, single):
        node = single.dummy.next

        assert node.x == 1
        assert node.next is single.dummy
        assert node.prev is single.dummy

    def test_create_from_nodes_rejects_invalid_n(self):
        dll = DLList()

        with pytest.raises(TypeError):
            dll.create_from_nodes("3", dll.dummy)

    def test_create_from_nodes_rejects_invalid_dummy(self):
        dll = DLList()

        with pytest.raises(TypeError):
            dll.create_from_nodes(0, None)


class TestDummyInvariants:
    def test_empty_dummy_points_to_self(self, empty):
        assert empty.dummy.next is empty.dummy
        assert empty.dummy.prev is empty.dummy

    def test_first_node_reachable_through_dummy_next(self, three):
        assert three.dummy.next.x == 1

    def test_last_node_reachable_through_dummy_prev(self, three):
        assert three.dummy.prev.x == 3

    def test_cycle_returns_to_dummy_from_front(self, three):
        assert three.dummy.next.next.next.next is three.dummy

    def test_cycle_returns_to_dummy_from_back(self, three):
        assert three.dummy.prev.prev.prev.prev is three.dummy

    def test_first_node_prev_points_to_dummy(self, three):
        assert three.dummy.next.prev is three.dummy

    def test_last_node_next_points_to_dummy(self, three):
        assert three.dummy.prev.next is three.dummy


class TestCheckSize:
    @pytest.mark.parametrize(
        "values",
        [
            [],
            [1],
            [1, 2, 3],
            [1, 2, 3, 4, 5],
        ],
    )
    def test_check_size_passes(self, values):
        dll = DLList(values)
        dll.check_size()

    def test_check_size_detects_corrupted_n(self, three):
        three.n = 999

        with pytest.raises(AssertionError):
            three.check_size()


class TestReverse:
    def test_reverse(self, three):
        three.reverse()

        assert three.to_list() == [3, 2, 1]

    def test_reverse_twice_restores_original(self, five):
        before = five.to_list()

        five.reverse()
        five.reverse()

        assert five.to_list() == before

    def test_reverse_empty_is_noop(self, empty):
        empty.reverse()

        assert empty.to_list() == []

    def test_reverse_single_is_noop(self, single):
        single.reverse()

        assert single.to_list() == [1]


class TestRotate:
    def test_rotate_zero_is_noop(self, five):
        before = five.to_list()

        five.rotate(0)

        assert five.to_list() == before

    def test_rotate_by_size_is_noop(self, five):
        before = five.to_list()

        five.rotate(five.size)

        assert five.to_list() == before

    def test_rotate_left(self, five):
        five.rotate(2)

        assert five.to_list() == [3, 4, 5, 1, 2]


class TestPalindrome:
    def test_even_palindrome(self):
        dll = DLList([1, 2, 2, 1])

        assert dll.is_palindrome() is True

    def test_odd_palindrome(self):
        dll = DLList([1, 2, 3, 2, 1])

        assert dll.is_palindrome() is True

    def test_non_palindrome(self):
        dll = DLList([1, 2, 3])

        assert dll.is_palindrome() is False

    def test_single_element_is_palindrome(self):
        dll = DLList([1])

        assert dll.is_palindrome() is True


class TestDeal:
    def test_deal_even_length(self):
        dll = DLList([0, 1, 2, 3, 4, 5])

        dealt = dll.deal()

        assert dll.to_list() == [0, 2, 4]
        assert dealt.to_list() == [1, 3, 5]

    def test_deal_odd_length(self):
        dll = DLList([0, 1, 2, 3, 4])

        dealt = dll.deal()

        assert dll.to_list() == [0, 2, 4]
        assert dealt.to_list() == [1, 3]

    def test_deal_preserves_all_elements(self):
        values = list(range(10))

        dll = DLList(values)
        dealt = dll.deal()

        combined = sorted(dll.to_list() + dealt.to_list())

        assert combined == values
