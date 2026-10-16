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
        if i < self.front.size:
            return self.front.get(i)
        else:
            return self.back.get(i - self.front.size)

    def set(self, i: int, x: Any) -> None:
        if i < self.front.size:
            return self.front.set(i, x)
        else:
            return self.back.set(i - self.front.size, x)

    def add_first(self, x: Any):
        self.add(0, x)

    def add_last(self, x: Any):
        self.add(self.size, x)

    def remove_first(self):
        self.remove(0)

    def remove_last(self):
        self.remove(self.size)

    # --------------------------------------------------------------
    # other public methods - with indexing etc...
    # --------------------------------------------------------------

    def add(self, i: int, x: Any) -> None:
        self._balance()
        if i < self.front.size:
            self.front.add(i, x)
        else:
            self.back.add(i - self.front.size, x)

    def remove(self, i: int) -> Any:
        self._balance()
        if i < self.front.size:
            self.front.add(i)
        else:
            self.back.add(i - self.front.size)

    # --------------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------------

    def _balance(self):
        mid = self.size // 2
        if self.front.size >= self.back.size * 3:
            while self.back.size < mid:
                self.back.add_first(self.front.remove_last())

        elif self.back.size >= self.front.size * 3:
            while self.front.size < mid:
                self.front.add_last(self.back.remove_first())

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
