from typing import Any

from ...base import BaseCollection
from .min_stack import MinStack


class MinDeque(BaseCollection):
    def __init__(self):
        self.front = MinStack()
        self.back = MinStack()

    @property
    def size(self):
        return self.front.size + self.back.size

    def get(self, i: int) -> Any:
        fs = self.front.size
        if i < fs:
            return self.front.get(fs - 1 - i)
        return self.back.get(i - fs)

    def add_first(self, x: Any):
        self.front.push(x)
        self._balance()

    def add_last(self, x: Any):
        self.back.push(x)
        self._balance()

    def remove_first(self) -> Any:
        if self.front.is_empty():
            if self.back.size == 1:
                return self.back.pop()
            self._balance()

        x = self.front.pop()
        self._balance()

        return x

    def remove_last(self) -> Any:
        if self.back.is_empty():
            if self.front.size == 1:
                return self.front.pop()
            self._balance()

        x = self.back.pop()
        self._balance()

        return x

    def get_min(self) -> int:
        if self.front.is_empty() and self.back.is_empty():
            raise IndexError("get_min from empty MinDeque")

        if self.front.is_empty():
            return self.back.get_min()

        if self.back.is_empty():
            return self.front.get_min()

        front_min = self.front.get_min()
        back_min = self.back.get_min()

        return front_min if front_min < back_min else back_min

    def __iter__(self):
        for x in reversed(list(self.front)):
            yield x
        for x in self.back:
            yield x

    def __repr__(self):
        if self.is_empty():
            return f"{self.__class__.__name__}([], min: None)"
        return f"{self.__class__.__name__}({list(self)}, min: {self.get_min()})"

    def __str__(self):
        out = [" MinDeque ".center(50, "=")]
        out.append(f"Front : {repr(self.front)}")
        out.append(f"Back  : {repr(self.back)}")
        out.append(f"Size  : {self.size}")
        out.append(f"Min   : {self.get_min()}")
        return "\n".join(out)

    def _balance(self):
        fs = self.front.size
        bs = self.back.size
        if fs == 0 or bs == 0 or 3 * fs < bs or 3 * bs < fs:
            mid = (self.size + 1) // 2

            f = MinStack()
            for i in reversed(range(mid)):
                f.push(self.get(i))

            b = MinStack()
            for i in range(mid, self.size):
                b.push(self.get(i))

            self.front = f
            self.back = b
