"""Shared test helpers for the contract-based test suites.

Imported by test_invariants.py, test_deque_ops.py and test_index_ops.py.
All helpers go through the public API only, so they work for every
implementation regardless of internal representation.
"""


def contents(seq):
    """Logical contents, front to back, read through the public API."""
    return [seq.get(i) for i in range(seq.size)]


def build_last(seq, values):
    """Fill seq in order via add_last and return it."""
    for v in values:
        seq.add_last(v)
    return seq


def build(seq, values):
    """Alias for build_last — fill via add(i, x) at the end."""
    for v in values:
        seq.add(seq.size, v)
    return seq


def drain_first(seq):
    """Remove every element via remove_first(); in order."""
    return [seq.remove_first() for _ in range(seq.size)]


def drain_last(seq):
    """Remove every element via remove_last(); returns back-to-front order."""
    return [seq.remove_last() for _ in range(seq.size)]


def drain_stack(seq):
    """Pop everything via pop(); returns back-to-front order (LIFO drain)."""
    return [seq.pop() for _ in range(seq.size)]


def drain_queue(seq):
    """Dequeue everything via remove(); returns front-to-back order (FIFO drain)."""
    return [seq.remove() for _ in range(seq.size)]


def add_item(seq, x):
    """Insert one element through whichever insert interface seq exposes.

    Invariants never care about position/order, so any insert endpoint
    works. Prefer the list facades, then stack push, then queue add.
    """
    if hasattr(seq, "add_last"):
        seq.add_last(x)
    elif hasattr(seq, "push"):
        seq.push(x)
    else:
        seq.add(x)


def remove_item(seq):
    """Remove one element through whichever remove interface seq exposes."""

    if hasattr(seq, "remove_last"):
        seq.remove_last()

    elif hasattr(seq, "pop"):
        seq.pop()

    elif hasattr(seq, "find"):
        x = seq.find(float("-inf"))
        seq.remove(x)

    else:
        seq.remove()
