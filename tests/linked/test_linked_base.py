"""
Shared linked-list behaviour.

These tests are intended for:
    * SLList
    * DLList

Already covered elsewhere:
    * get/set/add/remove       -> test_index_ops.py
    * size/is_empty invariants -> test_invariants.py
    * stack contract           -> test_stack_ops.py
    * queue contract           -> test_queue_ops.py
"""

import pytest

from ods.linked import DLList, SLList

LINKED_IMPLS = [
    SLList,
    DLList,
]


def _param_ids(cls):
    return cls.__name__


@pytest.fixture(params=LINKED_IMPLS, ids=_param_ids)
def linked(request):
    return request.param


class TestConstructor:
    @pytest.mark.parametrize(
        "source",
        [
            [],
            [1],
            [1, 2, 3],
            tuple(range(5)),
            range(10),
        ],
    )
    def test_construct_from_iterable(self, linked, source):
        s = linked(source)
        assert s.to_list() == list(source)
        assert s.size == len(source)

    def test_construct_from_generator(self, linked):
        s = linked(x * 2 for x in range(5))
        assert s.to_list() == [0, 2, 4, 6, 8]
        assert s.size == 5


class TestIteration:
    def test_iteration_preserves_order(self, linked):
        s = linked([1, 2, 3, 4, 5])
        assert list(s) == [1, 2, 3, 4, 5]

    def test_to_list_matches_iteration(self, linked):
        s = linked([1, 2, 3, 4, 5])
        assert s.to_list() == list(s)

    def test_iteration_does_not_mutate_structure(self, linked):
        s = linked([1, 2, 3])

        before = s.to_list()
        list(s)

        assert s.to_list() == before
        assert s.size == 3


class TestRepresentation:
    def test_repr_contains_class_name(self, linked):
        s = linked([1, 2, 3])

        r = repr(s)

        assert linked.__name__ in r

    def test_repr_on_empty_structure(self, linked):
        s = linked()

        r = repr(s)

        assert linked.__name__ in r


class TestMixedOperations:
    def test_size_tracks_mixed_operations(self, linked):
        s = linked()

        s.add(0, 1)
        s.add(1, 2)
        s.add(2, 3)

        assert s.size == 3

        s.remove(0)
        s.remove(s.size - 1)

        assert s.size == 1
        assert s.to_list() == [2]

    def test_build_and_drain(self, linked):
        s = linked()

        for i in range(20):
            s.add(s.size, i)

        assert s.to_list() == list(range(20))

        while not s.is_empty():
            s.remove(0)

        assert s.size == 0
        assert s.to_list() == []

    def test_random_add_remove_matches_reference(self, linked):
        s = linked()
        ref = []

        for i in range(25):
            s.add(s.size, i)
            ref.append(i)

        for _ in range(10):
            s.remove(0)
            ref.pop(0)

        assert s.to_list() == ref
