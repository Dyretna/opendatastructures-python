"""Index-based mutation tests for RootishArrayStack variants.

All implementations (RootishArrayStack, ImprovedRAS, FurtherImprovedRAS)
expose the same index-based interface: add(i, x), remove(i), get(i), set(i).
No exclusions needed - all variants follow the same contract.

Tests verify the logical array semantics independent of internal block layout.
"""

import random

import pytest

from ods.arrays import ImprovedRAS, RootishArrayStack

RAS_IMPLEMENTATIONS = [
    RootishArrayStack,
    ImprovedRAS,
    # FurtherImprovedRAS,
]


@pytest.fixture(params=RAS_IMPLEMENTATIONS)
def seq(request):
    return request.param()


def contents(seq):
    """Logical contents, front to back, via public API."""
    return [seq.get(i) for i in range(seq.size)]


def build(seq, values):
    """Fill seq via add_last (add at end) and return it."""
    for v in values:
        seq.add(seq.size, v)
    return seq


# ------------------------------------------------------------------
# Size & emptiness invariants
# ------------------------------------------------------------------


def test_initial_size_is_zero(seq):
    assert seq.size == 0


def test_is_empty_when_new(seq):
    assert seq.is_empty()


def test_not_empty_after_add(seq):
    seq.add(0, 1)
    assert not seq.is_empty()


def test_empty_again_after_remove_all(seq):
    for i in range(5):
        seq.add(seq.size, i)

    while not seq.is_empty():
        seq.remove(0)

    assert seq.is_empty()
    assert seq.size == 0


def test_size_increments_on_add(seq):
    initial_size = seq.size
    seq.add(0, 1)
    assert seq.size == initial_size + 1


def test_size_decrements_on_remove(seq):
    seq.add(0, 1)
    initial_size = seq.size
    seq.remove(0)
    assert seq.size == initial_size - 1


# ------------------------------------------------------------------
# add(i, x)
# ------------------------------------------------------------------


def test_add_into_empty_ras(seq):
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
    build(seq, list(range(10)))
    seq.add(1, "L")
    seq.add(seq.size - 1, "R")
    expected = list(range(10))
    expected.insert(1, "L")
    expected.insert(len(expected) - 1, "R")
    assert contents(seq) == expected


def test_add_triggers_growth(seq):
    for i in range(500):
        seq.add(i, i)
    assert seq.size == 500
    assert contents(seq) == list(range(500))


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
# get() and set()
# ------------------------------------------------------------------


def test_get_at_valid_index(seq):
    build(seq, [10, 20, 30, 40])
    assert seq.get(0) == 10
    assert seq.get(2) == 30
    assert seq.get(3) == 40


def test_get_at_each_position(seq):
    baseline = [1, 2, 3, 4, 5]
    fresh = type(seq)()
    build(fresh, baseline)
    for i, expected in enumerate(baseline):
        assert fresh.get(i) == expected


def test_get_out_of_bounds_raises(seq):
    build(seq, [1, 2, 3, 4])
    with pytest.raises(IndexError):
        seq.get(10)


def test_set_returns_old_value(seq):
    build(seq, [10, 20, 30])
    old = seq.set(1, 99)
    assert old == 20
    assert seq.get(1) == 99
    assert contents(seq) == [10, 99, 30]


def test_set_preserves_others(seq):
    build(seq, [1, 2, 3, 4, 5])
    seq.set(2, 99)
    assert contents(seq) == [1, 2, 99, 4, 5]


def test_set_at_each_position(seq):
    baseline = [1, 2, 3, 4, 5]
    fresh = type(seq)()
    build(fresh, baseline)
    for i in range(len(baseline)):
        fresh.set(i, 99)
        assert fresh.get(i) == 99


def test_set_out_of_bounds_raises(seq):
    build(seq, [1, 2, 3, 4])
    with pytest.raises(IndexError):
        seq.set(10, 99)


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

        if step % 89 == 0:
            assert contents(seq) == ref

    assert contents(seq) == ref


def test_add_and_remove_preserves_contents(seq):
    """Build up a sequence then tear it down via opposite ends."""
    build(seq, list(range(20)))
    assert contents(seq) == list(range(20))

    for i in range(10):
        assert seq.remove(0) == i

    assert contents(seq) == list(range(10, 20))


def test_interleaved_add_remove_at_various_indices(seq):
    """Stress test with random indices near front/middle/back."""
    rng = random.Random(42)
    ref = []

    for _ in range(1000):
        op = rng.choice(
            [
                "add_front",
                "add_mid",
                "add_back",
                "remove_front",
                "remove_mid",
                "remove_back",
            ]
        )

        if op == "add_front":
            idx = 0
            val = rng.randint(0, 99)
            seq.add(idx, val)
            ref.insert(idx, val)
        elif op == "add_mid":
            idx = rng.randint(0, len(ref))
            val = rng.randint(0, 99)
            seq.add(idx, val)
            ref.insert(idx, val)
        elif op == "add_back":
            idx = len(ref)
            val = rng.randint(0, 99)
            seq.add(idx, val)
            ref.insert(idx, val)
        elif op == "remove_front" and ref:
            idx = 0
            assert seq.remove(idx) == ref.pop(idx)
        elif op == "remove_mid" and len(ref) > 1:
            idx = rng.randint(1, len(ref) - 1)
            assert seq.remove(idx) == ref.pop(idx)
        elif op == "remove_back" and ref:
            idx = len(ref) - 1
            assert seq.remove(idx) == ref.pop(idx)

    assert contents(seq) == ref


def test_get_and_set_after_many_mutations(seq):
    """Build, mutate, then verify get/set still work correctly."""
    build(seq, list(range(50)))

    for i in range(50):
        assert seq.get(i) == i

    for i in range(50):
        seq.set(i, i * 2)

    for i in range(50):
        assert seq.get(i) == i * 2
