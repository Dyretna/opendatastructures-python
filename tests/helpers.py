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
    """Remove every element from the front, in order."""
    return [seq.remove_first() for _ in range(seq.size)]


def drain_last(seq):
    """Remove every element from the back, in order (front to back)."""
    return [seq.remove_last() for _ in range(seq.size)]
