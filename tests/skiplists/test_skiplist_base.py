import pytest

from ods.skip_list import SkiplistSSet, SkiplistWithFinger, SkiplistWithRank

SSET_IMPLEMENTATIONS = [
    SkiplistSSet,
    SkiplistWithRank,
    SkiplistWithFinger,
]


@pytest.fixture(params=SSET_IMPLEMENTATIONS)
def sl(request):
    return request.param()


class TestheightHandling:
    def test_height_growth_does_not_break_structure(self, sl, monkeypatch):
        heights = iter([4, 3, 2, 1, 0])

        def fake_height():
            return next(heights)

        monkeypatch.setattr(sl, "_pick_height", fake_height)

        for v in [10, 20, 30, 40, 50]:
            sl.add(v)

        assert sl.to_list() == [10, 20, 30, 40, 50]
        assert len(sl) == 5
