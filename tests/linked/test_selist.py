# tests/linked/test_selist.py

import random

import pytest

from ods.linked import SEList


@pytest.fixture
def empty():
    return SEList()


@pytest.fixture
def three():
    s = SEList()

    for x in [1, 2, 3]:
        s.append(x)

    return s


@pytest.fixture
def many():
    s = SEList(block_size=4)

    for i in range(50):
        s.append(i)

    return s


class TestConstructor:
    def test_empty_structure(self, empty):
        assert empty.size == 0
        assert empty.dummy.next is empty.dummy
        assert empty.dummy.prev is empty.dummy

    def test_custom_block_size(self):
        s = SEList(block_size=4)

        assert s.b == 4

    def test_append_builds_structure(self):
        s = SEList()

        for i in range(10):
            s.append(i)

        assert s.to_list() == list(range(10))


class TestBlockInvariants:
    def test_empty_dummy_points_to_self(self, empty):
        assert empty.dummy.next is empty.dummy
        assert empty.dummy.prev is empty.dummy

    def test_non_empty_cycle_is_valid(self, many):
        assert many.dummy.next.prev is many.dummy
        assert many.dummy.prev.next is many.dummy

    def test_all_nodes_link_both_directions(self, many):
        u = many.dummy.next

        while u is not many.dummy:
            assert u.next.prev is u
            assert u.prev.next is u
            u = u.next

    def test_each_block_respects_capacity(self, many):
        u = many.dummy.next

        while u is not many.dummy:
            assert u.d.size <= u.d.capacity
            u = u.next


class TestLocationTraversal:
    def test_get_front_middle_back(self, many):
        assert many.get(0) == 0
        assert many.get(25) == 25
        assert many.get(49) == 49

    def test_set_front_middle_back(self, many):
        many.set(0, "a")
        many.set(25, "b")
        many.set(49, "c")

        assert many.get(0) == "a"
        assert many.get(25) == "b"
        assert many.get(49) == "c"


class TestAppend:
    def test_append_preserves_order(self):
        s = SEList()

        for i in range(100):
            s.append(i)

        assert s.to_list() == list(range(100))

    def test_append_creates_multiple_nodes(self):
        s = SEList(block_size=4)

        for i in range(30):
            s.append(i)

        count = 0
        u = s.dummy.next

        while u is not s.dummy:
            count += 1
            u = u.next

        assert count > 1


class TestBalancingOperations:
    def test_many_front_insertions(self):
        s = SEList(block_size=4)

        values = []

        for i in range(50):
            s.add(0, i)
            values.insert(0, i)

        assert s.to_list() == values

    def test_many_middle_insertions(self):
        s = SEList(block_size=4)

        values = []

        for i in range(50):
            idx = len(values) // 2

            s.add(idx, i)
            values.insert(idx, i)

        assert s.to_list() == values

    def test_many_front_removals(self):
        s = SEList(block_size=4)

        values = list(range(100))

        for x in values:
            s.append(x)

        for expected in values:
            assert s.remove(0) == expected

        assert s.is_empty()

    def test_many_middle_removals(self):
        s = SEList(block_size=4)

        values = list(range(50))

        for x in values:
            s.append(x)

        while values:
            idx = len(values) // 2

            expected = values.pop(idx)
            actual = s.remove(idx)

            assert actual == expected

        assert s.is_empty()

    def test_random_operations_match_reference_list(self):
        s = SEList(block_size=4)

        ref = []
        rng = random.Random(42)

        for _ in range(300):
            if not ref or rng.random() < 0.6:
                i = rng.randint(0, len(ref))
                v = rng.randint(0, 1000)

                s.add(i, v)
                ref.insert(i, v)
            else:
                i = rng.randrange(len(ref))

                assert s.remove(i) == ref.pop(i)

            assert s.to_list() == ref


class TestNodeLifecycle:
    def test_draining_structure_removes_all_nodes(self):
        s = SEList(block_size=4)

        for i in range(40):
            s.append(i)

        while not s.is_empty():
            s.remove(0)

        assert s.dummy.next is s.dummy
        assert s.dummy.prev is s.dummy

    def test_size_matches_iteration(self, many):
        assert len(list(many)) == many.size


class TestLargeOperations:
    def test_large_append(self):
        s = SEList(block_size=8)

        for i in range(500):
            s.append(i)

        assert s.size == 500
        assert s.get(0) == 0
        assert s.get(499) == 499

    def test_large_front_insertions(self):
        s = SEList(block_size=8)

        for i in range(250):
            s.add(0, i)

        assert s.size == 250
        assert s.to_list() == list(reversed(range(250)))

    def test_large_front_removals(self):
        s = SEList(block_size=8)

        for i in range(250):
            s.append(i)

        for expected in range(250):
            assert s.remove(0) == expected

        assert s.size == 0
