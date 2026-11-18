import pytest

from ods.linked import DLList


class TestAbsorb:
    def test_absorb_preserves_order(self):
        l1 = DLList([1, 2, 3])
        l2 = DLList([4, 5, 6])

        l1.absorb(l2)

        assert l1.to_list() == [1, 2, 3, 4, 5, 6]

    def test_absorb_updates_size(self):
        l1 = DLList([1, 2, 3])
        l2 = DLList([4, 5])

        l1.absorb(l2)

        assert l1.size == 5

    def test_absorb_empties_second_list(self):
        l1 = DLList([1, 2, 3])
        l2 = DLList([4, 5])

        l1.absorb(l2)

        assert l2.size == 0
        assert l2.to_list() == []

    def test_absorb_into_empty_list(self):
        l1 = DLList()
        l2 = DLList([1, 2, 3])

        l1.absorb(l2)

        assert l1.to_list() == [1, 2, 3]
        assert l1.size == 3

    def test_absorb_single_element_lists(self):
        l1 = DLList([1])
        l2 = DLList([2])

        l1.absorb(l2)

        assert l1.to_list() == [1, 2]

    def test_absorb_cycle_remains_valid(self):
        l1 = DLList([1, 2, 3])
        l2 = DLList([4, 5, 6])

        l1.absorb(l2)

        l1.check_size()

        assert l1.dummy.next.prev is l1.dummy
        assert l1.dummy.prev.next is l1.dummy

    def test_absorb_resets_l2_dummy_cycle(self):
        l1 = DLList([1, 2, 3])
        l2 = DLList([4, 5, 6])

        l1.absorb(l2)

        assert l2.dummy.next is l2.dummy
        assert l2.dummy.prev is l2.dummy

    def test_absorb_empty_list_raises(self):
        l1 = DLList([1, 2, 3])
        l2 = DLList()

        with pytest.raises(IndexError):
            l1.absorb(l2)

    def test_absorb_sizes_are_conserved(self):
        l1 = DLList(list(range(10)))
        l2 = DLList(list(range(10, 20)))

        total = l1.size + l2.size

        l1.absorb(l2)

        assert l1.size == total
        assert l2.size == 0
