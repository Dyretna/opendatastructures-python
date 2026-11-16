from typing import Any

from ...base import BaseCollection
from ..array_deque import OrderedDeque


class MinDeque(BaseCollection):
    def __init__(self):
        self.main_deque = OrderedDeque()
        self.aux_deque = OrderedDeque()

    @property
    def size(self):
        return self.aux_deque.n

    def add_first(self, x: Any):
        self.main_deque.add_first(x)

        if self.size == 0:
            self.aux_deque.add_first(x)
        elif x > self.aux_deque.a[self.aux_deque.block_start]:
            self.aux_deque.add_first(self.aux_deque.a[self.aux_deque.block_start])
        else:
            self.aux_deque.add_first(x)

    def add_last(self, x: Any):
        self.main_deque.add_last(x)

        if self.size == 0:
            self.aux_deque.add_last(x)
        elif x > self.aux_deque.a[self.aux_deque.block_end]:
            self.aux_deque.add_last(self.aux_deque.a[self.aux_deque.block_end])
        else:
            self.aux_deque.add_last(x)

    def pop_left(self) -> Any:
        self.main_deque.remove_first()
        self.aux_deque.remove_first()

    def pop_right(self) -> Any:
        self.main_deque.remove_last()
        self.aux_deque.remove_first()

    def get_min(self):
        first = self.aux_deque.a[self.aux_deque.block_start]
        last = self.aux_deque.a[self.aux_deque.block_end]
        if first <= last:
            return first
        else:
            return last

    def __str__(self):
        out = [" MinDeque ".center(40, "=")]
        out.append(f"MainDeque: {self.main_deque.a}")
        out.append(f"AuxDeque: {self.aux_deque.a}")
        out.append(f"Size: {self.size}")
        out.append(f"Min: {self.get_min()}")
        return "\n".join(out)
