import random

from ods.arrays import ArrayStack


def assert_matches_python_list(s: ArrayStack, ref: list):
    assert s.size == len(ref)

    for i in range(len(ref)):
        assert s.get(i) == ref[i]


# --------------------------------------------------
# stack abstract interface methods: push() and pop()
# --------------------------------------------------


def test_push_pop():
    s = ArrayStack()

    for i in range(20):
        s.push(i)

    for i in range(19, -1, -1):
        assert s.pop() == i


# ----------------------------------------------
# get() and set()
# ----------------------------------------------


def test_get_and_set():
    s = ArrayStack()
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
    s = ArrayStack()

    s.add(0, 10)

    old = s.set(0, 20)

    assert old == 10
    assert s.get(0) == 20


# ----------------------------------------------
# add_all()
# ----------------------------------------------


def test_empty_stack():
    s = ArrayStack()

    assert s.size == 0


def test_add_all_and_size():
    s = ArrayStack()

    s.add_all(0, list(range(100)))

    assert s.size == 100


def test_add_all_middle_insert():
    s = ArrayStack()

    s.add(0, 1)
    s.add(1, 9)
    s.add_all(1, [2, 3, 4, 5, 6, 7, 8])

    assert [s.get(i) for i in range(s.size)] == [1, 2, 3, 4, 5, 6, 7, 8, 9]


# ----------------------------------------------
# test add()
# ----------------------------------------------


def test_append_using_add():
    s = ArrayStack()

    s.add(0, 10)
    s.add(1, 20)
    s.add(2, 30)

    assert s.size == 3
    assert s.get(0) == 10
    assert s.get(1) == 20
    assert s.get(2) == 30


def test_add_front():
    s = ArrayStack()

    s.add(0, 3)
    s.add(0, 2)
    s.add(0, 1)

    assert [s.get(i) for i in range(s.size)] == [1, 2, 3]


def test_add_middle():
    s = ArrayStack()

    s.add(0, 1)
    s.add(1, 3)

    s.add(1, 2)

    assert [s.get(i) for i in range(s.size)] == [1, 2, 3]


# ----------------------------------------------
# test remove()
# ----------------------------------------------


def test_remove_last():
    s = ArrayStack()

    for x in [1, 2, 3]:
        s.add(s.size, x)

    assert s.remove(2) == 3

    assert [s.get(i) for i in range(s.size)] == [1, 2]


# ----------------------------------------------
# test _resize()
# ----------------------------------------------


def test_grow_on_full_capacity():
    s = ArrayStack()
    assert s.capacity == 4

    s.add(0, "x")
    assert s.capacity == 4

    s.add_all(0, list(range(4)))
    assert s.capacity == 8


def test_shrink_when_array_becomes_sparse():
    s = ArrayStack()

    for i in range(10):
        s.add(s.size, i)

    initial_capacity = s.capacity

    while s.size > 0:
        s.remove(s.size - 1)

    assert s.capacity < initial_capacity


def test_capacity_invariant():
    s = ArrayStack()

    for i in range(1000):
        s.add(s.size, i)

        assert len(s.a) >= s.n
        assert s.capacity >= s.n

    while s.n > 0:
        s.remove(s.n - 1)

        assert len(s.a) >= s.n
        assert len(s.a) >= s.n
        assert s.capacity >= s.n


def test_many_grows_and_shrinks():
    s = ArrayStack()
    ref = []

    for i in range(500):
        s.add(s.size, i)
        ref.append(i)

    for _ in range(450):
        assert s.remove(s.size - 1) == ref.pop()

    assert s.size == len(ref)

    for i, x in enumerate(ref):
        assert s.get(i) == x


# ----------------------------------------------
# test reference match and random operations
# ----------------------------------------------


def test_random_operations():
    random.seed(42)

    s = ArrayStack()
    ref = []

    for _ in range(5000):
        if len(ref) == 0:
            operation = "add"
        else:
            operation = random.choice(["add", "remove", "set"])

        if operation == "add":
            i = random.randrange(len(ref) + 1)
            x = random.randint(0, 100000)

            s.add(i, x)
            ref.insert(i, x)

        elif operation == "remove":
            i = random.randrange(len(ref))

            assert s.remove(i) == ref.pop(i)

        else:
            i = random.randrange(len(ref))
            x = random.randint(0, 100000)

            assert s.set(i, x) == ref[i]
            ref[i] = x

        assert_matches_python_list(s, ref)
