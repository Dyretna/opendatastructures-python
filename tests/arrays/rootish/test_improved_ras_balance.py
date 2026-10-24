from ods.arrays import ImprovedRAS


def assert_balanced(seq):
    if seq.size > 4:
        assert not (3 * seq.front_n < seq.back_n or 3 * seq.back_n < seq.front_n)


def test_balance_after_many_front_adds():
    seq = ImprovedRAS()

    for i in range(100):
        seq.add(0, i)

    assert seq.size == 100
    assert seq._contents() == list(reversed(range(100)))
    assert seq.front_n + seq.back_n == seq.size
    assert_balanced(seq)


def test_balance_after_many_back_adds():
    seq = ImprovedRAS()

    for i in range(100):
        seq.add(seq.size, i)

    assert seq.size == 100
    assert seq._contents() == list(range(100))
    assert seq.front_n + seq.back_n == seq.size
    assert_balanced(seq)


def test_balance_preserves_contents_front_heavy():
    seq = ImprovedRAS()
    ref = []

    for i in range(50):
        seq.add(0, i)
        ref.insert(0, i)

    assert seq._contents() == ref


def test_balance_preserves_contents_back_heavy():
    seq = ImprovedRAS()
    ref = []

    for i in range(50):
        seq.add(seq.size, i)
        ref.append(i)

    assert seq._contents() == ref


def test_balance_after_many_front_removes():
    seq = ImprovedRAS()

    for i in range(100):
        seq.add(seq.size, i)

    for _ in range(80):
        seq.remove(0)

    assert seq._contents() == list(range(80, 100))
    assert seq.front_n + seq.back_n == seq.size
    assert_balanced(seq)


def test_balance_after_many_back_removes():
    seq = ImprovedRAS()

    for i in range(100):
        seq.add(seq.size, i)

    for _ in range(80):
        seq.remove(seq.size - 1)

    assert seq._contents() == list(range(20))
    assert seq.front_n + seq.back_n == seq.size
    assert_balanced(seq)


def test_balance_after_mixed_operations():
    seq = ImprovedRAS()
    ref = []

    for i in range(200):
        seq.add(0, i)
        ref.insert(0, i)

    for _ in range(75):
        seq.remove(0)
        ref.pop(0)

    for i in range(50):
        seq.add(seq.size, i)
        ref.append(i)

    assert seq._contents() == ref
    assert seq.front_n + seq.back_n == seq.size
    assert_balanced(seq)


def test_balance_keeps_all_elements_reachable():
    seq = ImprovedRAS()

    for i in range(250):
        seq.add(0, i)

    result = [seq.get(i) for i in range(seq.size)]

    assert result == list(reversed(range(250)))
