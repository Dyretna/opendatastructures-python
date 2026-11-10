import random

import pytest

from ods.skip_list import SkiplistWithFinger


@pytest.fixture
def sl():
    return SkiplistWithFinger()


class TestFindBasics:
    def test_find_on_empty_list(self, sl):
        assert sl.find(10) is None

    def test_find_existing_values(self, sl):
        for v in [1, 3, 5, 7, 9]:
            sl.add(v)

        assert sl.find(1) == 1
        assert sl.find(5) == 5
        assert sl.find(9) == 9

    def test_find_returns_successor(self, sl):
        for v in [1, 3, 5, 7, 9]:
            sl.add(v)

        assert sl.find(0) == 1
        assert sl.find(2) == 3
        assert sl.find(4) == 5
        assert sl.find(8) == 9

    def test_find_returns_none_when_no_successor(self, sl):
        for v in [1, 3, 5]:
            sl.add(v)

        assert sl.find(10) is None


class TestFingerBehaviour:
    def test_repeated_finds_give_consistent_results(self, sl):
        for v in range(0, 50, 5):
            sl.add(v)

        # same query twice in a row: second call starts from the finger
        for v in range(50):
            first = sl.find(v)
            second = sl.find(v)
            assert first == second

    def test_find_after_add(self, sl):
        for v in [10, 20, 30]:
            sl.add(v)

        assert sl.find(15) == 20

        sl.add(25)  # mutation invalidates the finger
        assert sl.find(15) == 20
        assert sl.find(24) == 25

    def test_find_after_remove(self, sl):
        for v in [10, 20, 30, 40]:
            sl.add(v)

        sl.find(30)  # leave a stale-ish finger behind
        sl.remove(30)  # removed node may still sit in the finger

        assert sl.find(25) == 40
        assert sl.find(10) == 10
        assert sl.find(30) == 40

    def test_full_scan_ascending_twice(self, sl):
        values = list(range(0, 50, 3))
        for v in values:
            sl.add(v)

        # two consecutive ascending scans -- worst case for stale fingers
        for _ in range(2):
            for v in range(51):
                exp = next((e for e in values if e >= v), None)
                assert sl.find(v) == exp

    def test_full_scan_descending(self, sl):
        values = list(range(0, 50, 3))
        for v in values:
            sl.add(v)

        for v in range(49, -1, -1):
            exp = next((e for e in values if e >= v), None)
            assert sl.find(v) == exp


class TestEdgeCases:
    def test_find_min_element(self, sl):
        for v in [5, 3, 1]:
            sl.add(v)

        assert sl.find(-100) == 1
        assert sl.find(0) == 1

    def test_find_max_element(self, sl):
        for v in [5, 3, 1]:
            sl.add(v)

        assert sl.find(5) == 5
        assert sl.find(6) is None

    def test_find_single_element(self, sl):
        sl.add(7)

        assert sl.find(7) == 7
        assert sl.find(6) == 7
        assert sl.find(8) is None


class TestRandomizedBehaviour:
    def test_random_mixed_ops_find_matches_reference(self, sl):
        reference = set()

        for _ in range(1000):
            v = random.randint(0, 100)
            op = random.random()

            if op < 0.5:
                if v in reference:
                    assert sl.add(v) is False
                else:
                    assert sl.add(v) is True
                    reference.add(v)
            elif op < 0.75:
                if v in reference:
                    assert sl.remove(v) is True
                    reference.remove(v)
                else:
                    assert sl.remove(v) is False
            else:
                succ = min((e for e in reference if e >= v), default=None)
                assert sl.find(v) == succ

    def test_random_sequence_of_finds_matches_sorted_list(self, sl):
        reference = set()
        values = list(range(100))
        random.shuffle(values)

        for v in values:
            sl.add(v)
            reference.add(v)

        sorted_vals = sorted(reference)
        for _ in range(500):
            v = random.randint(-10, 110)
            succ = next((e for e in sorted_vals if e >= v), None)
            assert sl.find(v) == succ
