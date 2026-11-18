import random

import pytest

from ods.linked import DLList


class TestTakeFirst:
    def test_take_first_moves_first_node(self):
        target = DLList([1, 2])
        source = DLList([3, 4, 5])

        target.take_first(source)

        assert target.to_list() == [1, 2, 3]
        assert source.to_list() == [4, 5]

    def test_take_first_updates_sizes(self):
        target = DLList([1])
        source = DLList([2, 3])

        target.take_first(source)

        assert target.size == 2
        assert source.size == 1

    def test_take_first_into_empty_list(self):
        target = DLList()
        source = DLList([1, 2, 3])

        target.take_first(source)

        assert target.to_list() == [1]
        assert source.to_list() == [2, 3]

    def test_take_first_from_empty_raises(self):
        target = DLList()
        source = DLList()

        with pytest.raises(IndexError):
            target.take_first(source)

    def test_take_first_preserves_dummy_cycle(self):
        target = DLList([1, 2])
        source = DLList([3, 4])

        target.take_first(source)

        target.check_size()
        source.check_size()

        assert target.dummy.next.prev is target.dummy
        assert target.dummy.prev.next is target.dummy


class TestMerge:
    def test_merge_two_sorted_lists(self):
        l1 = DLList([1, 3, 5])
        l2 = DLList([2, 4, 6])

        merged = DLList.merge(l1, l2)

        assert merged.to_list() == [1, 2, 3, 4, 5, 6]

    def test_merge_preserves_duplicates(self):
        l1 = DLList([1, 2, 2, 5])
        l2 = DLList([2, 3, 4])

        merged = DLList.merge(l1, l2)

        assert merged.to_list() == [1, 2, 2, 2, 3, 4, 5]

    def test_merge_left_smaller_than_right(self):
        l1 = DLList([1, 2])
        l2 = DLList([10, 20, 30, 40])

        merged = DLList.merge(l1, l2)

        assert merged.to_list() == [1, 2, 10, 20, 30, 40]

    def test_merge_right_smaller_than_left(self):
        l1 = DLList([10, 20, 30, 40])
        l2 = DLList([1, 2])

        merged = DLList.merge(l1, l2)

        assert merged.to_list() == [1, 2, 10, 20, 30, 40]

    def test_merge_empties_both_inputs(self):
        l1 = DLList([1, 3, 5])
        l2 = DLList([2, 4, 6])

        DLList.merge(l1, l2)

        assert l1.size == 0
        assert l2.size == 0

        assert l1.to_list() == []
        assert l2.to_list() == []

    def test_merge_result_has_valid_cycle(self):
        l1 = DLList([1, 3, 5])
        l2 = DLList([2, 4, 6])

        merged = DLList.merge(l1, l2)

        merged.check_size()

        assert merged.dummy.next.prev is merged.dummy
        assert merged.dummy.prev.next is merged.dummy


class TestSort:
    def test_sort_empty(self):
        dll = DLList()

        dll.sort()

        assert dll.to_list() == []

    def test_sort_single_element(self):
        dll = DLList([1])

        dll.sort()

        assert dll.to_list() == [1]

    def test_sort_already_sorted(self):
        dll = DLList([1, 2, 3, 4, 5])

        dll.sort()

        assert dll.to_list() == [1, 2, 3, 4, 5]

    def test_sort_reverse_sorted(self):
        dll = DLList([5, 4, 3, 2, 1])

        dll.sort()

        assert dll.to_list() == [1, 2, 3, 4, 5]

    def test_sort_with_duplicates(self):
        dll = DLList([5, 2, 5, 1, 2, 4])

        dll.sort()

        assert dll.to_list() == [1, 2, 2, 4, 5, 5]

    def test_sort_random_values(self):
        values = [9, 4, 1, 7, 3, 8, 5, 2, 6]

        dll = DLList(values)

        dll.sort()

        assert dll.to_list() == sorted(values)

    def test_sort_preserves_size(self):
        values = [5, 1, 4, 2, 3]

        dll = DLList(values)

        dll.sort()

        assert dll.size == len(values)

    def test_sort_result_has_valid_cycle(self):
        dll = DLList([9, 7, 5, 3, 1])

        dll.sort()

        dll.check_size()

        assert dll.dummy.next.prev is dll.dummy
        assert dll.dummy.prev.next is dll.dummy

    def test_sort_many_random_trials(self):
        rng = random.Random(108)

        for _ in range(100):
            values = [rng.randint(0, 1000) for _ in range(25)]

            dll = DLList(values)

            dll.sort()

            assert dll.to_list() == sorted(values)
