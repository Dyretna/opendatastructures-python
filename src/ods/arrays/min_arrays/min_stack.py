from typing import Any

from ...base import BaseCollection
from ..array_stack import ArrayStack


class MinStack(BaseCollection):
    def __init__(self):
        self.main_stack = ArrayStack()
        self.aux_stack = ArrayStack()

    @property
    def size(self):
        return self.aux_stack.n

    def get(self, i: int) -> Any:
        return self.main_stack.get(i)

    def push(self, x: Any):
        self.main_stack.add(self.size, x)

        if self.is_empty():
            self.aux_stack.add(self.size, x)
        elif x >= self.aux_stack.get(self.size - 1):
            self.aux_stack.add(self.size, self.aux_stack.get(self.size - 1))
        else:
            self.aux_stack.add(self.size, x)

    def pop(self) -> Any:
        i = self.size - 1
        self.aux_stack.remove(i)
        return self.main_stack.remove(i)

    def get_min(self):
        return self.aux_stack.get(self.size - 1)

    def __iter__(self):
        for x in self.main_stack:
            yield x

    def __repr__(self):
        if self.is_empty():
            return f"{self.__class__.__name__}([], min: None)"
        return f"{self.__class__.__name__}({list(self)}, min: {self.get_min()})"

    def __str__(self):
        out = [" MinStack ".center(50, "=")]
        out.append(f"MainStack : {self.main_stack.a}")
        out.append(f"AuxStack  : {self.aux_stack.a}")
        out.append(f"Size      : {self.size}")
        out.append(f"Min       : {self.get_min()}")
        return "\n".join(out)
