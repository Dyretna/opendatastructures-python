import random

import pytest

from ods.skip_list.skiplist_list import SkiplistList


@pytest.fixture
def flat_heights(monkeypatch):
    """Force all node heights to 0 for deterministic structure tests."""
    monkeypatch.setattr(SkiplistList, "_pick_height", lambda self: 0)


def _build(values, heights=None):
    """Build a SkiplistList from values; optionally feed heights."""
    sl = SkiplistList()
    if heights is not None:
        it = iter(heights)
        SlList = SkiplistList
        orig = SlList._pick_height
        SlList._pick_height = lambda self: next(it)
        try:
            for i, x in enumerate(values):
                sl.add(i, x)
        finally:
            SlList._pick_height = orig
    else:
        for i, x in enumerate(values):
            sl.add(i, x)
    return sl


def _dump_level(sl, r):
    u = sl.sentinel

    print(f"\nLEVEL {r}")

    while True:
        nxt = u.next[r].x if r <= u.height and u.next[r] else None

        print(f"x={u.x}, len={u.length[r]}, next={nxt}")

        if u.next[r] is None:
            break

        u = u.next[r]


class TestContentsAndSizes:  # (deterministic, flat heights)
    def test_absorb_appends_in_order(self, flat_heights):
        l1 = _build([1, 2, 3])
        l2 = _build([4, 5, 6])

        l1.absorb(l2)

        assert l1.to_list() == [1, 2, 3, 4, 5, 6]
        assert len(l1) == 6
        assert l1.n == 6

    def test_absorb_empties_l2_completely(self, flat_heights):
        l1 = _build([1, 2, 3])
        l2 = _build([4, 5, 6])

        l1.absorb(l2)

        assert l2.to_list() == []
        assert len(l2) == 0
        assert l2.n == 0
        assert l2.h == 0
        assert l2.sentinel.next == [None]
        assert l2.sentinel.length == [0]

    def test_absorb_correctly_sets_size(self, flat_heights):
        l1 = _build([1, 2, 3])
        l2 = _build([4, 5, 6])

        l1.absorb(l2)

        assert l1.n == 6

    def test_absorb_into_empty_self(self, flat_heights):
        l1 = SkiplistList()
        l2 = _build([10, 20, 30])

        l1.absorb(l2)

        assert l1.to_list() == [10, 20, 30]
        assert len(l1) == 3
        assert l2.to_list() == []

    def test_absorb_empty_l2_is_a_noop(self, flat_heights):
        # absorbing an empty list must not crash and must not
        # change self: exercises levels where l2 has no nodes
        l1 = _build([1, 2, 3])
        l2 = SkiplistList()

        l1.absorb(l2)

        assert l1.to_list() == [1, 2, 3]
        assert len(l1) == 3
        assert l2.to_list() == []

    def test_absorb_both_empty(self, flat_heights):
        l1 = SkiplistList()
        l2 = SkiplistList()

        l1.absorb(l2)

        assert l1.to_list() == []
        assert len(l1) == 0

    def test_absorb_single_elements(self, flat_heights):
        l1 = _build([1])
        l2 = _build([2])

        l1.absorb(l2)

        assert l1.to_list() == [1, 2]
        assert l1.get(0) == 1
        assert l1.get(1) == 2


class TestStructuralInvariants:
    def test_sentinel_arrays_stay_parallel_in_both_lists(self, flat_heights):
        # absorb raises l2.h and appends only to next (not length) --
        # the arrays must stay the same length in BOTH lists
        l1 = _build(list(range(10)))
        l2 = _build(list(range(10, 20)))

        l1.absorb(l2)

        assert len(l1.sentinel.next) == len(l1.sentinel.length)
        assert len(l2.sentinel.next) == len(l2.sentinel.length)

    def test_merged_height_covers_tallest_node(self, flat_heights):
        # after absorb, every non-None top level must be reachable:
        # sentinel.next[h] must not be None for a non-empty list
        l1 = _build(list(range(10)))
        l2 = _build(list(range(10, 20)))

        l1.absorb(l2)

        assert l1.sentinel.next[l1.h] is not None

    def test_dead_levels_extend_to_new_end(self):
        heights1 = [0, 1, 2, 3] + [0] * 6
        l1 = _build(list(range(10)), heights=heights1)
        l2 = _build(list(range(10, 20)), heights=[0] * 10)

        l1.absorb(l2)

        print("After Absorb - Dead Levels".center(50, "-"))

        # level 1..3 exist only in l1
        for r in range(1, l1.h + 1):
            _dump_level(l1, r)

            total = 0
            u = l1.sentinel

            while u.next[r] is not None:
                total += u.length[r]
                u = u.next[r]

            assert total + u.length[r] == l1.n + 1, f"level {r}"

    def test_connected_levels_preserve_length_convention(self):
        heights1 = [0, 1, 2, 3] + [0] * 6
        heights2 = [0, 1, 2, 3] + [0] * 6

        l1 = _build(list(range(10)), heights=heights1)
        l2 = _build(list(range(10, 20)), heights=heights2)

        print("Before Absorb - L1".center(50, "-"))
        for r in range(l1.h + 1):
            _dump_level(l1, r)

        print("Before Absorb - L2".center(50, "-"))
        for r in range(l2.h + 1):
            _dump_level(l2, r)

        expected = {}
        for r in range(l1.h + 1):
            total = 0
            u = l1.sentinel

            while u.next[r] is not None:
                total += u.length[r]
                u = u.next[r]

            expected[r] = total + u.length[r]

            print(f"Level {r}: before={expected[r]}")

        l1.absorb(l2)

        print("After Absorb".center(50, "-"))

        for r in range(l1.h + 1):
            _dump_level(l1, r)

            total = 0
            u = l1.sentinel

            while u.next[r] is not None:
                total += u.length[r]
                u = u.next[r]

            after = total + u.length[r]

            print(
                f"Level {r}: "
                f"before={expected[r]}, "
                f"after={after}, "
                f"delta={after - expected[r]}"
            )

            # Whatever convention existed before absorb
            # must still hold afterwards.
            assert after == expected[r] + 10, (
                f"connected level {r}: expected {expected[r] + 10}, got {after}"
            )

        assert l1.n == 20
        assert l2.n == 0

    def test_level0_seam_is_connected(self):
        l1 = _build(list(range(10)), heights=[0] * 10)
        l2 = _build(list(range(10, 20)), heights=[0] * 10)

        l1.absorb(l2)

        print("After Absorb - Seam".center(50, "-"))
        _dump_level(l1, 0)

        u = l1.sentinel.next[0]

        while u.x != 9:
            u = u.next[0]

        assert u.next[0].x == 10


class TestUsabilityAfterAbsorb:  # stale book-keeping
    def test_merged_list_is_usable_after_absorb(self, flat_heights):
        l1 = _build(list(range(10)))
        l2 = _build(list(range(10, 20)))

        l1.absorb(l2)
        _dump_level(l1, 0)

        # reads must work across the former boundary
        assert l1.get(9) == 9
        assert l1.get(10) == 10
        assert l1.get(19) == 19

        # writes on both sides of the seam
        assert l1.set(5, 500) == 5
        l1.set(5, 5)  # reset
        assert l1.remove(12) == 12
        assert l1.add(0, -1) is None or True  # must not raise
        assert l1.to_list() == (
            [-1] + list(range(10)) + list(range(10, 12)) + list(range(13, 20))
        )

    def test_emptied_l2_is_reusable(self, flat_heights):
        # after being emptied, l2 must behave like a fresh list
        l1 = _build([1, 2, 3])
        l2 = _build([4, 5, 6])

        l1.absorb(l2)

        l2.add(0, 99)
        assert l2.to_list() == [99]
        assert l2.get(0) == 99
        l2.add(1, 100)
        assert l2.remove(0) == 99
        assert l2.to_list() == [100]

    def test_repeated_absorbs(self, flat_heights):
        # absorbing several lists in a row stresses the end-of-level
        # walk and the dead-level bookkeeping
        lists = [_build([i]) for i in range(5)]

        for i in range(1, 5):
            lists[0].absorb(lists[i])

        assert lists[0].to_list() == [0, 1, 2, 3, 4]
        assert all(len(x) == 0 for x in lists[1:])


class TestRandomizedComparisons:
    def test_randomized_absorb_against_python_list(self):
        rng1 = random.Random(111)
        rng2 = random.Random(222)

        for trial in range(200):
            # ----------------------------------------------
            # Build two independent SkiplistLists (l1, l2) and two
            # Python-list reference models.
            # Populate with random insertions.
            # ----------------------------------------------
            l1 = SkiplistList()
            l2 = SkiplistList()

            expected1 = []
            expected2 = []

            for _ in range(rng1.randint(0, 30)):
                i = rng1.randint(0, len(expected1))
                x = rng1.randint(0, 999)

                l1.add(i, x)
                expected1.insert(i, x)

            for _ in range(rng2.randint(0, 30)):
                i = rng2.randint(0, len(expected2))
                x = rng2.randint(0, 999)

                l2.add(i, x)
                expected2.insert(i, x)

            # ----------------------------------------------
            # Absorb l2 into l1.
            # ----------------------------------------------
            l1.absorb(l2)

            expected1.extend(expected2)
            expected2 = []

            # ----------------------------------------------
            # Verify observable behaviour matches the
            # Python-list reference model.
            # ----------------------------------------------
            assert l1.to_list() == expected1, f"trial {trial}: merged contents mismatch"

            assert l2.to_list() == [], f"trial {trial}: l2 not emptied"

            assert len(l1) == len(expected1), f"trial {trial}: l1 length mismatch"

            assert len(l2) == 0, f"trial {trial}: l2 length mismatch"

            # ----------------------------------------------
            # Basic structural sanity checks.
            # ----------------------------------------------
            assert len(l1.sentinel.next) == len(l1.sentinel.length), (
                f"trial {trial}: l1 sentinel arrays out of sync"
            )

            assert len(l2.sentinel.next) == len(l2.sentinel.length), (
                f"trial {trial}: l2 sentinel arrays out of sync"
            )

            # A non-empty list should have a node reachable
            # from the top level.
            if expected1:
                assert l1.sentinel.next[l1.h] is not None, (
                    f"trial {trial}: l1 top level disconnected"
                )

            # ----------------------------------------------
            # Continue mutating the merged result.
            #
            # Many absorb bugs do not show up immediately.
            # They only surface when later add/remove
            # operations traverse the modified structure.
            # ----------------------------------------------
            for _ in range(5):
                # Random removal.
                if expected1 and rng1.random() < 0.6:
                    j = rng1.randint(0, len(expected1) - 1)
                    print(l1.to_list())
                    print(f"trial={trial}, remove_index={j}, expected={expected1[j]}")

                    assert l1.remove(j) == expected1.pop(j)

                # Random insertion.
                if expected1 and rng1.random() < 0.6:
                    j = rng1.randint(0, len(expected1))
                    x = rng1.randint(0, 999)

                    l1.add(j, x)
                    expected1.insert(j, x)

                # After every operation, compare against
                # the reference model.
                assert l1.to_list() == expected1, (
                    f"trial {trial}: post-absorb mutation mismatch"
                )
