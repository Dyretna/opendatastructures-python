from typing import Any, Optional

from .original import ArrayDeque


class BoundedDeque(ArrayDeque):
    def __init__(self, b: Optional[int] = 3):
        self.a = [None] * (b + 1)
        self.j = 0
        self.n = 0

    @property
    def capacity(self):
        return len(self.a)

    def is_full(self):
        return self.size == self.capacity

    def add(self, i: int, x: Any):
        if self.is_full():
            raise ValueError("Bounded Deque is full")

        super().add(i, x)

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
