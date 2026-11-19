import pytest

from ods.skip_list import SkiplistWithFinger


@pytest.fixture
def sl():
    return SkiplistWithFinger()


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
