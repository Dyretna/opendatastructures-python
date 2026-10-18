"""Index-based mutation tests for deques.

Included: ArrayDeque, DualArrayDeque, NoModDeque
Excluded: BoundedDeque  (fixed capacity, no resize)
          OrderedDeque  (no index-based mutation)

"""

import random

import pytest

from ods.arrays import ArrayDeque, DualArrayDeque, NoModDeque

DEQUE_IMPLEMENTATIONS = [
    ArrayDeque,
    DualArrayDeque,
    NoModDeque,
]


@pytest.fixture(params=DEQUE_IMPLEMENTATIONS)
def seq(request):
    return request.param()


# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------


def contents(seq):
    """Logical contents, front to back, read through the public API."""
    return [seq.get(i) for i in range(seq.size)]


def build(seq, values):
    """Fill seq in order via add_last and return it."""
    for v in values:
        seq.add_last(v)
    return seq


# ------------------------------------------------------------------
# add(i, x)
# ------------------------------------------------------------------


def test_add_into_empty_deque(seq):
    seq.add(0, "a")
    assert seq.size == 1
    assert contents(seq) == ["a"]


def test_add_at_front(seq):
    build(seq, [1, 2, 3])
    seq.add(0, 0)
    assert contents(seq) == [0, 1, 2, 3]


def test_add_at_end(seq):
    build(seq, [1, 2, 3])
    seq.add(seq.size, 4)
    assert contents(seq) == [1, 2, 3, 4]


def test_add_in_middle(seq):
    build(seq, [1, 2, 4, 5])
    seq.add(2, 3)
    assert contents(seq) == [1, 2, 3, 4, 5]


def test_add_increments_size_by_one(seq):
    build(seq, [1, 2, 3])
    before = seq.size
    seq.add(1, 99)
    assert seq.size == before + 1


def test_add_at_every_position(seq):
    for i in range(4):
        fresh = type(seq)()
        build(fresh, [1, 2, 3])
        fresh.add(i, 99)

        expected = [1, 2, 3]
        expected.insert(i, 99)

        assert contents(fresh) == expected


def test_add_then_remove_same_index_restores_state(seq):
    build(seq, [1, 2, 3, 4])
    before = contents(seq)

    for i in range(len(before) + 1):
        seq.add(i, 99)
        assert seq.remove(i) == 99
        assert contents(seq) == before


def test_add_near_front_and_near_back(seq):
    """Exercises both shift directions inside add()."""
    build(seq, list(range(10)))

    seq.add(1, "L")  # left branch
    seq.add(seq.size - 1, "R")  # right branch

    expected = list(range(10))
    expected.insert(1, "L")
    expected.insert(len(expected) - 1, "R")

    assert contents(seq) == expected


def test_add_after_wraparound(seq):
    """Force j away from 0, then insert at the front."""
    build(seq, [1, 2, 3, 4, 5, 6])

    for _ in range(3):
        seq.remove(0)

    assert contents(seq) == [4, 5, 6]

    seq.add(0, 3)
    seq.add(0, 2)

    assert contents(seq) == [2, 3, 4, 5, 6]


def test_add_triggers_growth(seq):
    for i in range(500):
        seq.add(0, i)

    assert seq.size == 500
    assert contents(seq) == list(reversed(range(500)))


@pytest.mark.parametrize("bad_index", [-1, 5])
def test_add_out_of_bounds_raises(seq, bad_index):
    build(seq, [1, 2, 3, 4])
    with pytest.raises(IndexError):
        seq.add(bad_index, 99)


# ------------------------------------------------------------------
# remove(i)
# ------------------------------------------------------------------


def test_remove_at_front(seq):
    build(seq, [1, 2, 3])
    assert seq.remove(0) == 1
    assert contents(seq) == [2, 3]


def test_remove_at_end(seq):
    build(seq, [1, 2, 3])
    assert seq.remove(seq.size - 1) == 3
    assert contents(seq) == [1, 2]


def test_remove_in_middle(seq):
    build(seq, [1, 2, 3, 4, 5])
    assert seq.remove(2) == 3
    assert contents(seq) == [1, 2, 4, 5]


def test_remove_decrements_size_by_one(seq):
    build(seq, [1, 2, 3])
    before = seq.size
    seq.remove(1)
    assert seq.size == before - 1


def test_remove_only_element(seq):
    seq.add(0, 42)
    assert seq.remove(0) == 42
    assert seq.size == 0
    assert seq.is_empty()


def test_remove_at_every_position(seq):
    baseline = [1, 2, 3, 4, 5]

    for i in range(len(baseline)):
        fresh = type(seq)()
        build(fresh, baseline)

        expected = list(baseline)
        expected.pop(i)

        assert fresh.remove(i) == baseline[i]
        assert contents(fresh) == expected


def test_remove_near_front_and_near_back(seq):
    """Exercises both shift directions inside remove()."""
    build(seq, list(range(10)))

    assert seq.remove(1) == 1
    assert seq.remove(seq.size - 1) == 9

    assert contents(seq) == [0, 2, 3, 4, 5, 6, 7, 8]


def test_remove_from_front_drains_in_order(seq):
    build(seq, list(range(10)))

    for expected in range(10):
        assert seq.remove(0) == expected

    assert seq.is_empty()


def test_remove_from_back_drains_in_reverse(seq):
    build(seq, list(range(10)))

    for expected in reversed(range(10)):
        assert seq.remove(seq.size - 1) == expected

    assert seq.is_empty()


def test_remove_from_empty_raises(seq):
    assert seq.is_empty()
    with pytest.raises(IndexError):
        seq.remove(0)


@pytest.mark.parametrize("bad_index", [-1, 4])
def test_remove_out_of_bounds_raises(seq, bad_index):
    build(seq, [1, 2, 3, 4])
    with pytest.raises(IndexError):
        seq.remove(bad_index)


def test_remove_triggers_shrink(seq):
    build(seq, list(range(200)))

    for _ in range(190):
        seq.remove(0)

    assert seq.size == 10
    assert contents(seq) == list(range(190, 200))


# ------------------------------------------------------------------
# mixed operations
# ------------------------------------------------------------------


def test_add_then_remove_alternating(seq):
    build(seq, [1, 2, 3])

    seq.add(0, 0)
    assert seq.remove(seq.size - 1) == 3
    seq.add(seq.size, 4)
    assert seq.remove(0) == 0

    assert contents(seq) == [1, 2, 4]


def test_queue_pattern(seq):
    """add at end, remove at front."""
    for i in range(50):
        seq.add(seq.size, i)

    for expected in range(50):
        assert seq.remove(0) == expected

    assert seq.is_empty()


def test_stack_pattern(seq):
    """add at end, remove at end."""
    for i in range(50):
        seq.add(seq.size, i)

    for expected in reversed(range(50)):
        assert seq.remove(seq.size - 1) == expected

    assert seq.is_empty()


def test_repeated_grow_and_shrink_cycles(seq):
    for _ in range(5):
        for i in range(100):
            seq.add(seq.size, i)
        assert seq.size == 100

        for _ in range(100):
            seq.remove(seq.size - 1)
        assert seq.size == 0
        assert seq.is_empty()


def test_capacity_never_below_size(seq):
    if not hasattr(seq, "capacity"):
        pytest.skip("implementation exposes no capacity")

    rng = random.Random(7)

    for _ in range(500):
        if seq.size == 0 or rng.random() < 0.6:
            seq.add(rng.randint(0, seq.size), rng.randint(0, 99))
        else:
            seq.remove(rng.randrange(seq.size))

        assert seq.capacity >= seq.size


def test_random_operations_match_reference_list(seq):
    rng = random.Random(20261018)
    ref = []

    for step in range(600):
        if not ref or rng.random() < 0.55:
            i = rng.randint(0, len(ref))
            v = rng.randint(0, 999)
            seq.add(i, v)
            ref.insert(i, v)
        else:
            i = rng.randrange(len(ref))
            assert seq.remove(i) == ref.pop(i)

        assert seq.size == len(ref)

        # full comparison is O(n); sample it instead of doing it every step
        if step % 89 == 0:
            assert contents(seq) == ref

    assert contents(seq) == ref
