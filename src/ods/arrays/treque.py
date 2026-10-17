from typing import Any

from .array_deque import ArrayDeque


class Treque:
    def __init__(self):
        self.front = ArrayDeque()
        self.back = ArrayDeque()

    # --------------------------------------------------------------
    # Deque interface operations
    # --------------------------------------------------------------

    @property
    def size(self):
        return self.front.n + self.back.n

    def get(self, i: int) -> Any:
        self._index_bounds_check(i)
        if i < self.front.size:
            return self.front.get(i)
        else:
            return self.back.get(i - self.front.size)

    def set(self, i: int, x: Any) -> None:
        self._index_bounds_check(i)
        if i < self.front.size:
            return self.front.set(i, x)
        else:
            return self.back.set(i - self.front.size, x)

    def add_first(self, x: Any):
        self.front.add_first(x)

    def add_last(self, x: Any):
        self.back.add_last(x)

    def remove_first(self):
        if self.size == 0:
            raise IndexError("Treque is empty")
        if self.front.n > 0:
            return self.front.remove_first()
        return self.back.remove_first()

    def remove_last(self):
        if self.size == 0:
            raise IndexError("Treque is empty")
        if self.back.n > 0:
            return self.back.remove_last()
        return self.front.remove_last()

    # --------------------------------------------------------------
    # other public methods - with indexing etc...
    # --------------------------------------------------------------

    def add(self, i: int, x: Any) -> None:
        self._index_bounds_check_adding(i)

        if i < self.front.size:
            self.front.add(i, x)
            if self.front.size >= self.back.size * 3:
                self._balance_front()
        else:
            self.back.add(i - self.front.size, x)
            if self.back.size >= self.front.size * 3:
                self._balance_back()

    def remove(self, i: int) -> Any:
        self._index_bounds_check(i)

        if i < self.front.size:
            x = self.front.remove(i)
            if self.back.size >= self.front.size * 3:
                self._balance_back()
        else:
            x = self.back.remove(i - self.front.size)
            if self.front.size >= self.back.size * 3:
                self._balance_front()

        return x

    # --------------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------------

    def _index_bounds_check(self, i: int):
        if not (0 <= i <= self.size - 1):
            raise IndexError("index not in range")

    def _index_bounds_check_adding(self, i: int):
        if not (0 <= i <= self.size):
            raise IndexError("index not in range")

    def _balance_back(self):
        mid = self.size // 2
        while self.front.size < mid:
            self.front.add_last(self.back.remove_first())

    def _balance_front(self):
        mid = self.size // 2
        while self.back.size < mid:
            self.back.add_first(self.front.remove_last())

    def _rotate_left(self, r: int):
        pass

    def _rotate_right(self, r: int):
        pass

    def __lshift__(self, r: int):
        self._rotate_left(r)

    def __rshift__(self, r: int):
        self._rotate_right(r)

    def __str__(self):
        out = [f" {__class__.__name__} ".center(50, "=")]
        ordered = [self.get(i) for i in range(self.size)]
        out.append(f"front      : {self.front.a}")
        out.append(f"back       : {self.back.a}")
        out.append(f"ordered    : {ordered}")
        out.append("-" * 50)
        out.append(f"size front : {self.front.size}")
        out.append(f"size back  : {self.back.size}")
        out.append(f"total size : {self.size}")
        return "\n" + "\n".join(out)
