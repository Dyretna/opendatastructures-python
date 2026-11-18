import pytest

from ods.linked import DLList


class TestTruncate:
    def test_truncate_middle(self):
        dll = DLList([0, 1, 2, 3, 4, 5])

        right = dll.truncate(3)

        assert dll.to_list() == [0, 1, 2]
        assert right.to_list() == [3, 4, 5]

    def test_truncate_front(self):
        dll = DLList([0, 1, 2, 3])

        right = dll.truncate(0)

        assert dll.to_list() == []
        assert right.to_list() == [0, 1, 2, 3]

    def test_truncate_last_element(self):
        dll = DLList([0, 1, 2, 3])

        right = dll.truncate(3)

        assert dll.to_list() == [0, 1, 2]
        assert right.to_list() == [3]

    def test_truncate_preserves_order(self):
        values = list(range(20))

        dll = DLList(values)
        right = dll.truncate(10)

        assert dll.to_list() + right.to_list() == values

    def test_truncate_sizes_sum_to_original(self):
        dll = DLList(list(range(15)))

        original_size = dll.size

        right = dll.truncate(5)

        assert dll.size + right.size == original_size

    def test_truncate_left_cycle_is_valid(self):
        dll = DLList([0, 1, 2, 3, 4])

        dll.truncate(2)

        dll.check_size()
        assert dll.dummy.next.prev is dll.dummy
        assert dll.dummy.prev.next is dll.dummy

    def test_truncate_right_cycle_is_valid(self):
        dll = DLList([0, 1, 2, 3, 4])

        right = dll.truncate(2)

        right.check_size()
        assert right.dummy.next.prev is right.dummy
        assert right.dummy.prev.next is right.dummy

    @pytest.mark.parametrize("i", [-1, 4])
    def test_truncate_invalid_index_raises(self, i):
        dll = DLList([0, 1, 2, 3])

        with pytest.raises(IndexError):
            dll.truncate(i)
