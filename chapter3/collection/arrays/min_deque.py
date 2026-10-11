from typing import Any

from .array_deque_ordered import ArrayDequeOrdered


class MinDeque:
    def __init__(self):
        self.main_deque = ArrayDequeOrdered()
        self.aux_deque = ArrayDequeOrdered()

    @property
    def size(self):
        return self.aux_deque.n

    def add_left(self, x:Any):
        self.main_deque.add_left(x)

        if self.size == 0:
            self.aux_deque.add_left(x)
        elif x > self.aux_deque.get(0):
            self.aux_deque.add_left(self.aux_deque.get(0))
        else:
            self.aux_deque.add_left(x)

    def add_right(self, x:Any):
        self.main_deque.add_right(x)

        if self.size == 0:
            self.aux_deque.add_right(x)
        elif x > self.aux_deque.get(self.size - 1):
            self.aux_deque.add_right(self.aux_deque.get(self.size - 1))
        else:
            self.aux_deque.add_right(x)


    def pop_left(self) -> Any:
        self.main_deque.pop_left()
        self.aux_deque.pop_left()

    def pop_right(self) -> Any:
        self.main_deque.pop_right()
        self.aux_deque.pop_right()

    def get_min(self):
        first = self.aux_deque.get(0)
        last = self.aux_deque.get(self.size - 1)
        if first <= last:
            return first
        else:
            return last


    # ------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------

    def __str__(self):
        out = [" MinQueue ".center(40, "=")]
        out.append(f"MainDeque: {self.main_deque.a}")
        out.append(f"AuxDeque: {self.aux_deque.a}")
        out.append(f"Size: {self.size}")
        out.append(f"Min: {self.get_min()}")
        return "\n".join(out)
