"""Rootish-specific structural tests.

Everything LOGICAL about these implementations (add/remove/get/set
semantics, growth, error handling, stress behaviour) is covered by the
contract suites:

  * tests/test_invariants.py  (seq    -> ALL_IMPLS)
  * tests/test_index_ops.py   (index_seq -> INDEX_IMPLS, includes both)

This module only tests what is unique to the block layout:

  1. i2b() index -> block mapping (triangular block boundaries)
  2. the O(sqrt(n)) memory invariant: block count stays proportional
     to the theoretical minimum after growth

Structural tests are guarded with hasattr and skip cleanly for variants
that rename or drop internals (ImprovedRAS specifics live in
test_improved_specific.py).
"""

import math

import pytest

from ods.arrays import ImprovedRAS, RootishArrayStack

RAS_VARIANTS = [
    RootishArrayStack,
    ImprovedRAS,
    # FurtherImprovedRAS,
]


@pytest.fixture(params=RAS_VARIANTS, ids=lambda c: c.__name__)
def ras_seq(request):
    return request.param()


def minimum_blocks(n: int) -> int:
    """Smallest b such that the triangular number b(b+1)/2 >= n."""
    return math.ceil((-1 + math.sqrt(1 + 8 * n)) / 2)


# ------------------------------------------------------------------
# i2b: absolute index -> block index
# ------------------------------------------------------------------

# Triangular boundaries: block b holds indices from b(b-1)/2 up to
# b(b+1)/2 - 1.  0->0, 1->1, 2->1, 3->2, 5->2, 6->3, 9->3, 10->4 ...
I2B_BOUNDARIES = [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (5, 2),
    (6, 3),
    (9, 3),
    (10, 4),
    (14, 4),
    (15, 5),
]


def test_i2b_at_block_boundaries(ras_seq):
    if not hasattr(ras_seq, "i2b"):
        pytest.skip("implementation has no i2b")

    for i, expected_block in I2B_BOUNDARIES:
        assert ras_seq.i2b(i) == expected_block


def test_i2b_is_monotonically_non_decreasing(ras_seq):
    """Crossing a block boundary must never decrease the block index."""
    if not hasattr(ras_seq, "i2b"):
        pytest.skip("implementation has no i2b")

    prev = ras_seq.i2b(0)
    for i in range(1, 60):
        b = ras_seq.i2b(i)
        assert b >= prev, f"i2b decreased at i={i}: {prev} -> {b}"
        prev = b


# ------------------------------------------------------------------
# O(sqrt(n)) memory invariant
# ------------------------------------------------------------------


def test_block_count_stays_near_minimum_after_growth(ras_seq):
    """After adding n elements the block count should be O(sqrt(n)),
    close to the triangular minimum, never linear in n."""
    blocks = getattr(ras_seq, "blocks", None)
    if blocks is None:
        pytest.skip("implementation exposes no block list")

    n = 1000
    for i in range(n):
        ras_seq.add(ras_seq.size, i)

    assert ras_seq.size == n
    lo = minimum_blocks(n)  # must be able to hold all elements
    hi = 2 * lo + 2  # loose O(sqrt(n)) ceiling
    assert len(blocks) >= lo
    assert len(blocks) <= hi


def test_block_capacities_cover_size(ras_seq):
    """Total capacity across blocks must be at least the size."""
    blocks = getattr(ras_seq, "blocks", None)
    if blocks is None:
        pytest.skip("implementation exposes no block list")

    for i in range(200):
        ras_seq.add(ras_seq.size, i)

    total_capacity = sum(len(block) for block in blocks)
    assert total_capacity >= ras_seq.size


# ------------------------------------------------------------------
# Sanity: logical contents survive block reallocations
# (cheap re-check local to this module; deep coverage lives in
# test_index_ops.py)
# ------------------------------------------------------------------


def test_contents_correct_across_many_block_growths(ras_seq):
    """Each new add roughly every triangular boundary spawns a block;
    make sure contents stay coherent well past the first few blocks."""
    for i in range(300):
        ras_seq.add(ras_seq.size, i)
        if i % 89 == 0:
            assert [ras_seq.get(k) for k in range(ras_seq.size)] == list(range(i + 1))

    assert ras_seq.size == 300
