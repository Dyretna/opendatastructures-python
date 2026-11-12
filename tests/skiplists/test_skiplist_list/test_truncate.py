import random

import pytest

from ods.skip_list.skiplist_list import SkiplistList


@pytest.fixture
def sl():
    return SkiplistList()


@pytest.fixture
def flat_heights(monkeypatch):
    """Force all node heights to 0 for deterministic structure tests."""
    monkeypatch.setattr(SkiplistList, "_pick_height", lambda self: 0)


class TestBasicSplitting:
    def test_truncate_middle_splits_correctly(self, sl, flat_heights):
        for i, x in enumerate(range(0, 100, 5)):  # 20 elements
            sl.add(i, x)

        tail = sl.truncate(10)

        assert sl.to_list() == [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
        assert tail.to_list() == [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
        assert len(sl) == 10
        assert len(tail) == 10
        assert sl.n == 10
        assert tail.n == 10

    @pytest.mark.parametrize(
        "i,head,tailvals",
        [
            (1, [0], [5, 10, 15, 20]),
            (3, [0, 5, 10], [15, 20]),
            (4, [0, 5, 10, 15], [20]),  # the element at index i belongs to the tail
        ],
    )
    def test_truncate_various_positions(self, sl, flat_heights, i, head, tailvals):
        for j, x in enumerate([0, 5, 10, 15, 20]):
            sl.add(j, x)

        tail = sl.truncate(i)

        assert sl.to_list() == head
        assert tail.to_list() == tailvals
        assert len(sl) == len(head)
        assert len(tail) == len(tailvals)


class TestEdgeCases:
    def test_truncate_zero_empties_head(self, sl, flat_heights):
        for i, x in enumerate([10, 20, 30]):
            sl.add(i, x)

        tail = sl.truncate(0)

        assert sl.to_list() == []
        assert len(sl) == 0
        assert sl.h == 0
        assert tail.to_list() == [10, 20, 30]
        assert len(tail) == 3

    def test_truncate_at_size_gives_empty_tail(self, sl, flat_heights):
        # i == n must be legal (like an insertion position), giving
        # an empty tail: requires validate_index_insert, not _access
        for i, x in enumerate([10, 20, 30]):
            sl.add(i, x)

        tail = sl.truncate(3)

        assert sl.to_list() == [10, 20, 30]
        assert tail.to_list() == []
        assert len(tail) == 0
        assert tail.h == 0

    def test_truncate_invalid_index_raises(self, sl, flat_heights):
        sl.add(0, 1)

        with pytest.raises(IndexError):
            sl.truncate(2)
        with pytest.raises(IndexError):
            sl.truncate(-1)


class TestHeightBookeeping:
    def test_tail_height_is_tallest_tail_node_height(self, sl, monkeypatch):
        # NOTE: add() raises the list height by AT MOST one level per
        # insertion, so a single tall node cannot lift h from 0 to 4.
        # Schedule gradually increasing heights 1,2,3,4 instead: each
        # insertion sits exactly one above the current h, so no cap
        # kicks in, and the node at index 3 ends up with height 4.
        # Extra zeros feed the post-truncate operations.
        schedule = [1, 2, 3, 4] + [0] * 20
        heights = iter(schedule)
        monkeypatch.setattr(SkiplistList, "_pick_height", lambda self: next(heights))

        for i, x in enumerate(range(12)):
            sl.add(i, x)
        assert sl.h == 4  # node at index 3 has height 4
        assert sl.sentinel.next[sl.h] is not None

        tail = sl.truncate(3)

        # the height-4 node (index 3) lands in the tail, and the cut
        # reaches level 4, so the tail height is exactly 4 (not 5)
        assert tail.h == 4
        assert tail.sentinel.height == tail.h
        for r in range(tail.h + 1):
            assert tail.sentinel.next[r] is not None

        # head keeps the nodes with heights 1,2,3 -> h trims to 3, not 0
        assert sl.h == 3
        assert sl.sentinel.next[sl.h] is not None

        # both lists must stay fully usable (the crash class)
        tail.add(0, 99)
        assert tail.get(0) == 99
        assert tail.remove(0) == 99
        assert tail.get(3) == 6
        sl.add(0, -1)
        assert sl.to_list() == [-1, 0, 1, 2]

    def test_flat_heights_tail_is_level_zero_only(self, sl, flat_heights):
        # with all node heights 0 there is no level above 0 anywhere,
        # so the tail must also have height 0 -- regression test
        # against the tail_h = r + 1 off-by-one
        for i in range(20):
            sl.add(i, i)

        tail = sl.truncate(10)

        assert sl.h == 0
        assert tail.h == 0
        assert tail.sentinel.height == 0


class TestUsabilityAfterTruncate:
    def test_tail_is_usable_after_truncate(self, sl, flat_heights):
        for i in range(20):
            sl.add(i, i)

        tail = sl.truncate(10)

        tail.add(0, 999)
        assert tail.get(0) == 999
        tail.add(tail.size, 1234)
        assert tail.get(tail.size - 1) == 1234
        assert tail.remove(0) == 999
        assert tail.to_list() == list(range(10, 20)) + [1234]

    def test_head_is_usable_after_truncate(self, sl, flat_heights):
        for i in range(20):
            sl.add(i, i)

        sl.truncate(10)

        sl.add(0, -1)
        assert sl.get(0) == -1
        assert sl.set(1, 555) == 0
        assert sl.remove(2) == 1
        assert sl.to_list() == [-1, 555] + list(range(2, 10))

    def test_level0_walk_matches_size_in_both_lists(self, sl, flat_heights):
        for i in range(20):
            sl.add(i, i)

        tail = sl.truncate(7)

        for lst in (sl, tail):
            count = 0
            u = lst.sentinel.next[0]
            while u is not None:
                count += 1
                u = u.next[0]
            assert count == lst.n

    def test_indices_stay_valid_after_truncate(self, sl, flat_heights):
        # get(i) on the tail must return the relabeled values,
        # i.e. the sentinel-offset length bookkeeping is correct
        values = list(range(0, 60, 3))
        for i, x in enumerate(values):
            sl.add(i, x)

        tail = sl.truncate(11)

        assert sl.to_list() == values[:11]
        for k in range(len(values[11:])):
            assert tail.get(k) == values[11 + k]


class TestRandomized:
    def test_randomized_against_python_list(self):
        rng = random.Random(108)
        for trial in range(200):
            sl = SkiplistList()
            expected = []

            for _ in range(rng.randint(1, 40)):
                i = rng.randint(0, len(expected))
                x = rng.randint(0, 999)
                sl.add(i, x)
                expected.insert(i, x)

            i = rng.randint(0, len(expected))
            tail = sl.truncate(i)
            exp_tail = expected[i:]
            expected = expected[:i]

            assert sl.to_list() == expected, f"trial {trial}: head mismatch"
            assert tail.to_list() == exp_tail, f"trial {trial}: tail mismatch"
            assert len(sl) == len(expected)
            assert len(tail) == len(exp_tail)

            # height invariants: h is the tallest node height, so the
            # top level of a non-empty list must hold a real pointer --
            # catches tail.h off-by-one in BOTH directions
            if expected:
                assert sl.sentinel.next[sl.h] is not None, (
                    f"trial {trial}: head top level"
                )
            if exp_tail:
                assert tail.sentinel.height == tail.h, (
                    f"trial {trial}: tail sentinel height"
                )
                if tail.h > 0:
                    assert tail.sentinel.next[tail.h] is not None, (
                        f"trial {trial}: tail top level"
                    )

            # keep operating on BOTH lists afterwards: the truncate
            # bug class (wrong tail.h, off-by-one lengths) only shows
            # up when the lists are used again
            for _ in range(5):
                if expected and rng.random() < 0.5:
                    j = rng.randint(0, len(expected) - 1)
                    assert sl.remove(j) == expected.pop(j)
                if exp_tail and rng.random() < 0.5:
                    j = rng.randint(0, len(exp_tail) - 1)
                    assert tail.remove(j) == exp_tail.pop(j)

                if expected and rng.random() < 0.5:
                    j = rng.randint(0, len(expected))
                    sl.truncate(j)
                    expected = expected[:j]
                if exp_tail and rng.random() < 0.5:
                    j = rng.randint(0, len(exp_tail))
                    tail.truncate(j)
                    exp_tail = exp_tail[:j]

                assert sl.to_list() == expected, f"trial {trial}: post-ops head"
                assert tail.to_list() == exp_tail, f"trial {trial}: post-ops tail"
