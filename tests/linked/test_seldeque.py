import pytest

from ods.linked import SELDeque


@pytest.fixture
def empty():
    return SELDeque()


@pytest.fixture
def three():
    d = SELDeque()
    d.add_last(1)
    d.add_last(2)
    d.add_last(3)
    return d


@pytest.fixture
def many():
    d = SELDeque(block_size=4)
    for i in range(20):
        d.add_last(i)
    return d


class TestDummyInvariants:
    def test_empty_dummy_points_to_self(self, empty):
        assert empty.dummy.next is empty.dummy
        assert empty.dummy.prev is empty.dummy

    def test_first_block_exists_after_insert(self, empty):
        empty.add_last(1)

        assert empty.dummy.next is not empty.dummy
        assert empty.dummy.prev is not empty.dummy

    def test_single_block_cycle_is_valid(self, three):
        block = three.dummy.next

        assert block.prev is three.dummy
        assert block.next is three.dummy

    def test_multi_block_cycle_is_valid(self, many):
        assert many.dummy.next.prev is many.dummy
        assert many.dummy.prev.next is many.dummy


class TestGetFirstGetLast:
    def test_get_first(self, three):
        assert three.get_first() == 1

    def test_get_last(self, three):
        assert three.get_last() == 3

    def test_get_first_after_removals(self):
        d = SELDeque()

        for i in range(5):
            d.add_last(i)

        d.remove_first()
        d.remove_first()

        assert d.get_first() == 2

    def test_get_last_after_removals(self):
        d = SELDeque()

        for i in range(5):
            d.add_last(i)

        d.remove_last()
        d.remove_last()

        assert d.get_last() == 2


class TestBlockCreation:
    def test_add_last_creates_multiple_blocks(self):
        d = SELDeque(block_size=4)

        for i in range(20):
            d.add_last(i)

        assert d.size == 20

        count = 0
        u = d.dummy.next

        while u != d.dummy:
            count += 1
            u = u.next

        assert count > 1

    def test_add_first_creates_multiple_blocks(self):
        d = SELDeque(block_size=4)

        for i in range(20):
            d.add_first(i)

        assert d.size == 20

        count = 0
        u = d.dummy.next

        while u != d.dummy:
            count += 1
            u = u.next

        assert count > 1


class TestBlockRemoval:
    def test_removing_everything_removes_all_blocks(self):
        d = SELDeque(block_size=4)

        for i in range(20):
            d.add_last(i)

        while not d.is_empty():
            d.remove_first()

        assert d.size == 0
        assert d.dummy.next is d.dummy
        assert d.dummy.prev is d.dummy

    def test_single_empty_block_removed_after_remove_first(self):
        d = SELDeque()

        d.add_last(1)

        assert d.remove_first() == 1

        assert d.dummy.next is d.dummy
        assert d.dummy.prev is d.dummy

    def test_single_empty_block_removed_after_remove_last(self):
        d = SELDeque()

        d.add_last(1)

        assert d.remove_last() == 1

        assert d.dummy.next is d.dummy
        assert d.dummy.prev is d.dummy


class TestRoundtripBehavior:
    def test_fifo_order(self):
        d = SELDeque()

        for i in range(20):
            d.add_last(i)

        out = [d.remove_first() for _ in range(20)]

        assert out == list(range(20))

    def test_reverse_fifo_order(self):
        d = SELDeque()

        for i in range(20):
            d.add_first(i)

        out = [d.remove_last() for _ in range(20)]

        assert out == list(range(20))

    def test_lifo_front(self):
        d = SELDeque()

        for i in range(20):
            d.add_first(i)

        out = [d.remove_first() for _ in range(20)]

        assert out == list(reversed(range(20)))

    def test_lifo_back(self):
        d = SELDeque()

        for i in range(20):
            d.add_last(i)

        out = [d.remove_last() for _ in range(20)]

        assert out == list(reversed(range(20)))
