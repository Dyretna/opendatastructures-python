from typing import Any

from ..array_stack import ArrayStack


class DualArrayDeque:
    def __init__(self):
        self.front = ArrayStack()
        self.back = ArrayStack()

    # ------------------------------------------------------
    # Abstract interface requirements
    # + convenience methods and properties
    # ------------------------------------------------------

    @property
    def size(self):
        return self.front.n + self.back.n

    def is_empty(self):
        return self.size == 0

    def add_first(self, x: Any):
        self.add(0, x)

    def add_last(self, x: Any):
        self.add(self.size, x)

    def remove_first(self) -> Any:
        return self.remove(0)

    def remove_last(self) -> Any:
        return self.remove(self.size - 1)

    # ---------------------------------
    # Additional public methods
    # ---------------------------------

    def get(self, i: int):
        if self.is_empty():
            raise IndexError("empty... ")
        self._index_bounds_check(i)

        if i < self.front.n:
            return self.front.get(self.front.n - i - 1)
        else:
            return self.back.get(i - self.front.n)

    def set(self, i: int, x: Any):
        if self.is_empty():
            raise IndexError("empty... ")
        self._index_bounds_check(i)

        if i < self.front.n:
            return self.front.set(self.front.n - i - 1, x)
        else:
            return self.back.set(i - self.front.n, x)

    def add(self, i: int, x: Any):
        self._index_bounds_check_adding(i)

        if i < self.front.n:
            self.front.add(self.front.n - i, x)
        else:
            self.back.add(i - self.front.n, x)
        self._balance()

    def remove(self, i: int) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty deque")
        self._index_bounds_check(i)

        if i < self.front.n:
            x = self.front.remove(self.front.n - i - 1)
        else:
            x = self.back.remove(i - self.front.n)

        self._balance()
        return x

    # ---------------------------------
    # internal helpers
    # ---------------------------------

    def _index_bounds_check(self, i: int):
        if not (0 <= i <= self.size - 1):
            raise IndexError("index not in range")

    def _index_bounds_check_adding(self, i: int):
        if not (0 <= i <= self.size):
            raise IndexError("index not in range")

    def _balance(self):
        n = self.size
        mid = n // 2

        if 3 * self.front.n < self.back.n or 3 * self.back.n < self.front.n:
            f = ArrayStack()
            for i in range(mid):
                f.add(i, self.get(mid - i - 1))

            b = ArrayStack()
            for i in range(n - mid):
                b.add(i, self.get(mid + i))

            self.front = f
            self.back = b
