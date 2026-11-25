"""SESSet-specific structural tests.

Level 4 of the test hierarchy: tests that only make sense for SESSet
(block-based skiplist). SSet contract behaviour (add/remove/find
semantics) is covered by test_sorted_set_ops.py for all implementations;
general skiplist height handling by test_skiplist_base.py.

"""

import random

import pytest

from ods.skip_list import SESSet

# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture(params=[2, 3, 5])
def b(request):
    return request.param


@pytest.fixture
def sesset(b):
    return SESSet(b=b)


# ------------------------------------------------------------------
# Structural helpers (SESSet-specific)
# ------------------------------------------------------------------


def blocks(s: SESSet) -> list:
    """Non-empty blocks on level 0, in order."""
    out = []
    u = s.sentinel.next[0]
    while u is not None:
        out.append(u)
        u = u.next[0]
    return out


def flatten(s: SESSet) -> list:
    elems = []
    for blk in blocks(s):
        elems.extend(blk.d.to_list())
    return elems


def block_sizes(s: SESSet) -> list[int]:
    return [blk.d.size for blk in blocks(s)]


def level_starts(s: SESSet) -> list[list]:
    """First element of every block, per level. Raises on empty blocks."""
    levels = []
    for r in range(s.h + 1):
        level, u = [], s.sentinel.next[r]
        while u is not None:
            assert u.d.size > 0, f"empty block on level {r}"
            level.append(u.d[0])
            u = u.next[r]
        levels.append(level)
    return levels


def assert_structure(s: SESSet, b: int):
    """Full structural invariant check."""
    sizes = block_sizes(s)
    assert all(1 <= size <= b + 1 for size in sizes), f"bad block sizes: {sizes}"

    for r, level in enumerate(level_starts(s)):
        for j in range(len(level) - 1):
            assert level[j] < level[j + 1], (
                f"level {r}: block starting at {level[j]} "
                f"comes after block starting at {level[j + 1]}"
            )

    elems = flatten(s)
    assert elems == sorted(elems), "global ordering broken"


def assert_tail_invariant(s: SESSet):
    """tail must be the last level-0 block and hold the maximum element;
    None if the set is empty."""
    bs = blocks(s)
    if not bs:
        assert s.tail is None, "tail should be None for empty set"
        return
    assert s.tail is bs[-1], "tail does not point at last block"
    assert s.tail.d[s.tail.d.size - 1] == max(flatten(s)), (
        "tail does not hold max element"
    )


def assert_no_dangling_links(s: SESSet):
    """Every node reachable on level r must exist in every lower level."""
    seen = [set() for _ in range(s.h + 1)]
    for r in range(s.h + 1):
        u = s.sentinel.next[r]
        while u is not None:
            seen[r].add(id(u))
            u = u.next[r]
    for r in range(1, s.h + 1):
        assert seen[r] <= seen[r - 1], (
            f"level {r} references block absent on level {r - 1}"
        )


# ------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------


class TestStructureInvariants:
    def test_structure_after_mixed_operations(self, sesset, b):
        rng = random.Random(7)
        reference = set()

        for _ in range(300):
            x = rng.randint(0, 100)

            if rng.random() < 0.5:
                added = sesset.add(x)
                assert added == (x not in reference)
                if added:
                    reference.add(x)

            elif x in reference:
                assert sesset.remove(x) is True
                reference.discard(x)

            else:
                assert sesset.remove(x) is False

            assert_structure(sesset, b)
            assert_tail_invariant(sesset)
            assert_no_dangling_links(sesset)
            assert flatten(sesset) == sorted(reference)


class TestTailBehaviour:
    def test_remove_at_tail_updates_tail(self, sesset, b):
        for x in range(1, 21):
            sesset.add(x)

        old_max = max(flatten(sesset))
        assert sesset.remove(old_max) is True
        assert_tail_invariant(sesset)
        assert sesset.find(old_max) is None

        # drain to empty through the tail
        while len(sesset):
            assert sesset.remove(max(flatten(sesset))) is True
            assert_tail_invariant(sesset)

        assert sesset.tail is None
        assert sesset.sentinel.next[0] is None

    def test_readd_after_drain_to_empty(self, sesset, b):
        for x in range(1, 11):
            sesset.add(x)
        for x in range(1, 11):
            sesset.remove(x)
        assert sesset.tail is None

        assert sesset.add(108) is True
        assert_tail_invariant(sesset)
        assert flatten(sesset) == [108]


class TestHeightBlockInteraction:
    def test_removal_of_tall_block_unlinks_all_levels(self, b):
        """Deterministic heights: force a tall block, drain around it,
        and check every level is unlinked."""
        s = SESSet(b=b)
        heights = iter([3, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        def fake_height():
            try:
                return next(heights)
            except StopIteration:
                return 0

        s._pick_height = fake_height

        for x in range(10):
            s.add(x)

        assert s.h >= 1, "setup failed: no tall block created"

        # remove the contents of the tallest block, one at a time
        tall = max(blocks(s), key=lambda blk: blk.height)
        while tall.d.size:
            x = tall.d[0]
            if not s.remove(x):
                break
            assert_no_dangling_links(s)

        assert_structure(s, b)
        assert_tail_invariant(s)

    def test_grow_shrink_cycles_keep_structure(self, sesset, b):
        for cycle in range(5):
            for x in range(cycle * 20, cycle * 20 + 20):
                sesset.add(x)
            assert_structure(sesset, b)
            for x in range(cycle * 20, cycle * 20 + 20):
                sesset.remove(x)
            assert_structure(sesset, b)
            assert_tail_invariant(sesset)


class TestBorrowBoundary:
    def test_borrow_never_empties_successor(self, sesset, b):
        """The core remove-invariant: the loan loop must leave the
        successor block with at least one element, so remove() itself
        never produces persistent empty blocks."""
        for x in range(1, 41):
            sesset.add(x)

        for x in range(1, 41):
            sesset.remove(x)
            assert_structure(sesset, b)  # first_keys() asserts size > 0 inside
            assert_tail_invariant(sesset)
