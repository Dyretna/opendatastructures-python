from ods.arrays import ArrayQueue


def assert_matches_python_list(s: ArrayQueue, ref: list):
    assert s.size == len(ref)

    for i in range(len(ref)):
        assert s.get(i) == ref[i]


# --------------------------------------------------
# stack abstract interface methods: add(), remove()
# --------------------------------------------------


def test_add_remove():
    q = ArrayQueue()

    for i in range(20):
        q.add(i)

    for i in range(20):
        assert q.remove() == i


# ----------------------------------------------
# get() and set()
# ----------------------------------------------


def test_get_and_set():
    s = ArrayQueue()
    s.a = ["a", "b", "c"]
    s.n = 3

    assert s.get(0) == "a"
    assert s.get(1) == "b"
    assert s.get(2) == "c"

    s.set(0, 1)
    s.set(1, "x")
    s.set(2, 3)

    assert s.get(0) == 1
    assert s.get(1) == "x"
    assert s.get(2) == 3


def test_set_returns_old_value():
    s = ArrayQueue()

    s.add(10)

    old = s.set(0, 20)

    assert old == 10
    assert s.get(0) == 20


# ----------------------------------------------
# test _resize()
# ----------------------------------------------


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


def test_many_grows_and_shrinks():
    q = ArrayQueue()
    ref = []

    for i in range(500):
        q.add(i)
        ref.append(i)

    for _ in range(450):
        assert q.remove() == ref.pop(0)

    assert q.size == len(ref)

    for i, x in enumerate(ref):
        assert q.get(i) == x
