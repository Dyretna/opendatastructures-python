from typing import Any, Optional

from ...validation import Validator as Val
from .original import ArrayDeque


class BoundedDeque(ArrayDeque):
    def __init__(self, b: Optional[int] = 3):
        self.a = [None] * (b + 1)
        self.j = 0
        self.n = 0

    def add(self, i: int, x: Any):
        if self.size == self.capacity:
            raise ValueError("Bounded Deque is full")
        Val.validate_index_insert(i, self.size)

        if self.size == 0:
            self.a[self.j] = x
            self.n += 1
            return

        if i < self.size // 2:
            self.j = (self.j - 1) % self.capacity
            for k in range(i):
                self._shift_section_left(k)
        else:
            for k in range(self.size, i, -1):
                self._shift_section_right(k)

        self.a[(self.j + i) % self.capacity] = x
        self.n += 1

    def __str__(self):
        out = [f" {__class__.__name__} ".center(50, "=")]
        out.append(f"a: {self.a}")
        out.append(f"j: {self.j}")
        out.append(f"size: {self.size}")
        out.append(f"capacity: {self.capacity}")
        return "\n".join(out)

    # change of array-size forbidden.
    def _resize_grow(self):
        pass

    def _resize_shrink(self):
        pass
