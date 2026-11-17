"""BaseCollection-invariants — ALL implementations."""

from helpers import add_item, remove_item


def test_initial_size_is_zero(seq):
    assert seq.size == 0


def test_is_empty_when_new(seq):
    assert seq.is_empty()


def test_not_empty_after_add(seq):
    add_item(seq, 1)
    assert not seq.is_empty()


def test_size_increments_on_add(seq):
    before = seq.size
    add_item(seq, 1)
    assert seq.size == before + 1


def test_size_decrements_on_remove(seq):
    add_item(seq, 1)
    remove_item(seq)
    assert seq.size == 0


def test_empty_again_after_remove_all(seq):
    for i in range(5):
        add_item(seq, i)
    while not seq.is_empty():
        remove_item(seq)
    assert seq.is_empty()
