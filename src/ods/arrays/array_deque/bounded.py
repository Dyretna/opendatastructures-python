from typing import Any, Optional

from .original_with_additions import ArrayDeque


class BoundedDeque(ArrayDeque):
    def __init__(self, capacity: Optional[int] = 4):
        self.a = [None] * capacity
        self.j = 0
        self.n = 0

    # ---------------------------------
    # Additional public properties and methods
    # ---------------------------------

    @property
    def capacity(self):
        return len(self.a)

    def add(self, i: int, x: Any):
        if self.size == self.capacity:
            raise Exception("Block full")

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
