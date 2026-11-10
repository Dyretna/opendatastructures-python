import random

from ods.skip_list import SkiplistWithGet


def test_random_ops_get_matches_reference():
    sl = SkiplistWithGet()
    reference = []

    for _ in range(500):
        v = random.randint(0, 100)
        if v in reference:
            assert sl.remove(v) is True
            reference.remove(v)
        else:
            assert sl.add(v) is True
            reference.append(v)

        for i in range(len(reference)):
            assert sl.get(i) == sorted(reference)[i]
