from ods.arrays import ArrayQueue


def test_grow_on_full_capacity():
    q = ArrayQueue()
    assert q.capacity == 4

    q.add("x")
    q.add("x")
    q.add("x")
    q.add("x")
    q.add("x")

    assert q.capacity == 8


def test_shrink_when_array_becomes_sparse():
    q = ArrayQueue()

    for i in range(10):
        q.add(i)

    initial_capacity = q.capacity

    while q.size > 0:
        q.remove()

    assert q.capacity < initial_capacity


def test_capacity_invariant():
    q = ArrayQueue()

    for i in range(1000):
        q.add(i)

        assert len(q.a) >= q.n
        assert q.capacity >= q.n

    while q.n > 0:
        q.remove()

        assert len(q.a) >= q.n
        assert len(q.a) >= q.n
        assert q.capacity >= q.n
