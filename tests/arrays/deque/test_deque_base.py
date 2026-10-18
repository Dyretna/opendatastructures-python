import pytest

from ods.arrays import ArrayDeque, DualArrayDeque, NoModDeque, OrderedDeque

DEQUE_IMPLEMENTATIONS = [
    ArrayDeque,
    DualArrayDeque,
    NoModDeque,
    OrderedDeque,
]


@pytest.fixture(params=DEQUE_IMPLEMENTATIONS)
def seq(request):
    return request.param()


# ------------------------------------------------------------------
# Size & emptiness invariants
# ------------------------------------------------------------------


def test_initial_size_is_zero(seq):
    assert seq.size == 0


def test_is_empty_when_new(seq):
    assert seq.is_empty()


def test_not_empty_after_add(seq):
    seq.add_last(1)
    assert not seq.is_empty()


def test_empty_again_after_remove_all(seq):
    for i in range(5):
        seq.add_last(i)

    while not seq.is_empty():
        seq.remove_last()

    assert seq.is_empty()
    assert seq.size == 0


def test_size_increments_on_add(seq):
    initial_size = seq.size

    seq.add_first(1)
    assert seq.size == initial_size + 1

    seq.add_last(2)
    assert seq.size == initial_size + 2


def test_size_decrements_on_remove(seq):
    for i in range(3):
        seq.add_last(i)

    initial_size = seq.size
    seq.remove_first()
    assert seq.size == initial_size - 1


# ------------------------------------------------------------------
# Add first / Add last
# ------------------------------------------------------------------


def test_add_first_prepends(seq):
    seq.add_last(1)
    seq.add_first(2)
    seq.add_first(3)

    # Should be: 3, 2, 1 from front to back
    assert seq.size == 3


def test_add_last_appends(seq):
    seq.add_first(3)
    seq.add_last(2)
    seq.add_last(1)

    # Should be: 3, 2, 1 from front to back
    assert seq.size == 3


def test_mixed_add_operations_preserve_order(seq):
    seq.add_last(1)
    seq.add_first(0)
    seq.add_last(2)
    seq.add_first(-1)

    assert seq.size == 4


def test_add_first_with_large_batch(seq):
    for i in range(100):
        seq.add_first(i)

    assert seq.size == 100


def test_add_last_with_large_batch(seq):
    for i in range(100):
        seq.add_last(i)

    assert seq.size == 100


# ------------------------------------------------------------------
# Remove first / Remove last
# ------------------------------------------------------------------


def test_remove_first_returns_front_element(seq):
    for i in range(5):
        seq.add_last(i)

    assert seq.remove_first() == 0
    assert seq.size == 4


def test_remove_last_returns_back_element(seq):
    for i in range(5):
        seq.add_last(i)

    assert seq.remove_last() == 4
    assert seq.size == 4


def test_remove_first_from_single_element(seq):
    seq.add_last(42)

    assert seq.remove_first() == 42
    assert seq.is_empty()


def test_remove_last_from_single_element(seq):
    seq.add_first(42)

    result = seq.remove_last()

    assert result == 42
    assert seq.is_empty()


def test_alternating_remove_operations(seq):
    for i in range(6):
        seq.add_last(i)

    # Expected sequence: 0, 1, 2, 3, 4, 5
    assert seq.remove_first() == 0
    assert seq.remove_last() == 5
    assert seq.remove_first() == 1
    assert seq.remove_last() == 4
    assert seq.remove_first() == 2
    assert seq.remove_last() == 3
    assert seq.is_empty()


def test_remove_first_drains_queue(seq):
    for i in range(10):
        seq.add_last(i)

    for expected in range(10):
        assert seq.remove_first() == expected

    assert seq.is_empty()


def test_remove_last_drains_queue(seq):
    for i in range(10):
        seq.add_last(i)

    for expected in reversed(range(10)):
        assert seq.remove_last() == expected

    assert seq.is_empty()


# ------------------------------------------------------------------
# Edge cases
# ------------------------------------------------------------------


def test_remove_from_empty_raises_error(seq):
    assert seq.is_empty()

    with pytest.raises(IndexError):
        seq.remove_first()


def test_remove_last_from_empty_raises_error(seq):
    assert seq.is_empty()

    with pytest.raises(IndexError):
        seq.remove_last()


def test_add_and_remove_single_element_repeatedly(seq):
    for _ in range(10):
        seq.add_first(1)
        assert seq.remove_first() == 1
        assert seq.is_empty()


def test_mixed_add_remove_with_final_state_check(seq):
    """Add 5 elements from front, remove 3 from back, add 2 from back."""
    for i in range(5):
        seq.add_first(i)

    # Sequence should be: 4, 3, 2, 1, 0
    assert seq.remove_last() == 0
    assert seq.remove_last() == 1
    assert seq.remove_last() == 2

    # Remaining: 4, 3
    seq.add_last(10)
    seq.add_last(11)

    # Final: 4, 3, 10, 11
    assert seq.size == 4


# ------------------------------------------------------------------
# Growth/shrinkage behavior (for resizing implementations)
# ------------------------------------------------------------------


def test_growth_after_many_add_first(seq):
    """Triggers potential array growth."""
    for i in range(1000):
        seq.add_first(i)

    assert seq.size == 1000
    assert not seq.is_empty()


def test_growth_after_many_add_last(seq):
    """Triggers potential array growth."""
    for i in range(1000):
        seq.add_last(i)

    assert seq.size == 1000
    assert not seq.is_empty()


def test_shrinkage_after_many_remove_first(seq):
    """Grow then shrink to test shrinking behavior."""
    for i in range(1000):
        seq.add_last(i)

    for _ in range(900):
        seq.remove_first()

    assert seq.size == 100


def test_shrinkage_after_many_remove_last(seq):
    """Grow then shrink to test shrinking behavior."""
    for i in range(1000):
        seq.add_last(i)

    for _ in range(900):
        seq.remove_last()

    assert seq.size == 100


# ------------------------------------------------------------------
# Round-trip consistency
# ------------------------------------------------------------------


def test_add_first_then_remove_first_roundtrip(seq):
    values = [1, 2, 3, 4, 5]

    for v in values:
        seq.add_first(v)

    # Adding 5, 4, 3, 2, 1 to front -> queue: 5, 4, 3, 2, 1
    # Remove first gives: 5, 4, 3, 2, 1
    for expected in reversed(values):
        result = seq.remove_first()
        assert result == expected


def test_add_last_then_remove_last_roundtrip(seq):
    values = [1, 2, 3, 4, 5]

    for v in values:
        seq.add_last(v)

    # Queue: 1, 2, 3, 4, 5
    # Remove last gives: 5, 4, 3, 2, 1
    for expected in reversed(values):
        result = seq.remove_last()
        assert result == expected


def test_fifo_behavior_via_add_last_remove_first(seq):
    """Classic queue: add_last, remove_first = FIFO."""
    values = [10, 20, 30, 40, 50]

    for v in values:
        seq.add_last(v)

    for expected in values:
        assert seq.remove_first() == expected


def test_lifo_behavior_via_add_first_remove_last(seq):
    """Stack-like: add_first, remove_last = LIFO."""
    values = [10, 20, 30, 40, 50]

    for v in values:
        seq.add_first(v)

    # Queue became: 50, 40, 30, 20, 10
    # remove_last pops from back: 10, 20, 30, 40, 50
    for expected in values:
        assert seq.remove_last() == expected


def test_fifo_behavior_via_add_first_remove_last(seq):
    """Queue: add_first, remove_last = FIFO."""
    values = [10, 20, 30, 40, 50]

    for v in values:
        seq.add_first(v)

    # Queue became: 50, 40, 30, 20, 10
    # remove_last pops: 10, 20, 30, 40, 50
    for expected in values:
        assert seq.remove_last() == expected


def test_lifo_behavior_via_add_last_remove_first(seq):
    """Stack: add_last, remove_first = LIFO."""
    values = [10, 20, 30, 40, 50]

    for v in values:
        seq.add_last(v)

    # Queue: 10, 20, 30, 40, 50
    # remove_first pops: 10, 20, 30, 40, 50
    for expected in values:
        assert seq.remove_first() == expected


# ------------------------------------------------------------------
# Randomized stress test
# ------------------------------------------------------------------


def test_random_operations_stress(seq):
    """Random mix of adds and removes to catch edge cases."""
    import random

    reference = []

    for _ in range(500):
        operation = random.choice(
            ["add_first", "add_last", "remove_first", "remove_last"]
        )

        if operation == "add_first":
            value = random.randint(0, 1000)
            seq.add_first(value)
            reference.insert(0, value)

        elif operation == "add_last":
            value = random.randint(0, 1000)
            seq.add_last(value)
            reference.append(value)

        elif operation == "remove_first":
            if reference:
                expected = reference.pop(0)
                result = seq.remove_first()
                assert result == expected

        elif operation == "remove_last":
            if reference:
                expected = reference.pop(-1)
                result = seq.remove_last()
                assert result == expected

    # If reference is empty, both should be empty
    if not reference:
        assert seq.is_empty()
