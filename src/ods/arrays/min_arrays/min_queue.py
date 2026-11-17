from typing import Any

from ...base import BaseCollection
from .min_stack import MinStack


class MinQueue(BaseCollection):
    def __init__(self):
        self.in_stack = MinStack()  # back of Queue
        self.out_stack = MinStack()  # front of Queue

    @property
    def size(self):
        return self.in_stack.size + self.out_stack.size

    def add(self, x: Any):
        self.in_stack.push(x)

    def remove(self) -> Any:
        if self.out_stack.is_empty():
            self._transfer()
        return self.out_stack.pop()

    def get_min(self) -> int:
        if self.in_stack.is_empty() and self.out_stack.is_empty():
            raise IndexError("get_min from empty MinQueue")

        if self.in_stack.is_empty():
            return self.out_stack.get_min()

        if self.out_stack.is_empty():
            return self.in_stack.get_min()

        in_min = self.in_stack.get_min()
        out_min = self.out_stack.get_min()
        return out_min if out_min < in_min else in_min

    def _transfer(self):
        while not self.in_stack.is_empty():
            self.out_stack.push(self.in_stack.pop())

    def __iter__(self):
        for x in reversed(list(self.out_stack)):
            yield x
        for x in self.in_stack:
            yield x

    def __repr__(self):
        if self.is_empty():
            return f"{self.__class__.__name__}([], min: None)"
        return f"{self.__class__.__name__}({list(self)}, min: {self.get_min()})"

    def __str__(self):
        out = [" MinQueue ".center(50, "=")]
        out.append(f"In   : {repr(self.in_stack)}")
        out.append(f"Out  : {repr(self.out_stack)}")
        out.append(f"Size : {self.size}")
        out.append(f"Min  : {self.get_min()}")
        return "\n".join(out)
