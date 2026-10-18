import pytest

from ods.arrays import BoundedDeque


def test_capacity_is_fixed_at_init():
    dq = BoundedDeque(capacity=5)
    assert dq.capacity == 5


def test_raises_on_capacity_exceeded():
    dq = BoundedDeque(capacity=3)

    dq.add_last(1)
    dq.add_last(2)
    dq.add_last(3)

    with pytest.raises(ValueError):
        dq.add_last(4)


def test_raises_when_full_add_first():
    dq = BoundedDeque(capacity=2)
    dq.add_last(1)
    dq.add_last(2)

    with pytest.raises(ValueError):
        dq.add_first(3)


def test_no_resize_happens_on_fill():
    dq = BoundedDeque(capacity=100)

    for i in range(100):
        dq.add_last(i)

    assert dq.capacity == 100


def test_can_use_after_partial_consume():
    dq = BoundedDeque(capacity=5)

    for i in range(5):
        dq.add_last(i)

    dq.remove_first()
    dq.remove_first()

    dq.add_last(10)
    dq.add_last(11)

    assert dq.size == 5


def test_default_capacity():
    dq = BoundedDeque()
    assert dq.capacity > 0
