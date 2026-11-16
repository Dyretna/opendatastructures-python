from typing import Any

from ...base import BaseList
from ...validation import Validator as Val
from ..array_stack import ArrayStack


class DualArrayDeque(BaseList):
    def __init__(self):
        self.front = ArrayStack()
        self.back = ArrayStack()

    @property
    def size(self):
        return self.front.n + self.back.n

    def get(self, i: int):
        if self.is_empty():
            raise IndexError("empty... ")
        Val.validate_index_access(i, self.size)

        if i < self.front.size:
            return self.front.get(self.front.n - i - 1)
        else:
            return self.back.get(i - self.front.n)

    def set(self, i: int, x: Any):
        if self.is_empty():
            raise IndexError("empty... ")
        Val.validate_index_access(i, self.size)

        if i < self.front.size:
            return self.front.set(self.front.n - i - 1, x)
        else:
            return self.back.set(i - self.front.n, x)

    def add(self, i: int, x: Any):
        Val.validate_index_insert(i, self.size)

        if i < self.front.n:
            self.front.add(self.front.n - i, x)
        else:
            self.back.add(i - self.front.n, x)
        self._balance()

    def remove(self, i: int) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty deque")
        Val.validate_index_access(i, self.size)

        if i < self.front.n:
            x = self.front.remove(self.front.n - i - 1)
        else:
            x = self.back.remove(i - self.front.n)

        self._balance()
        return x

    # ---------------------------------
    # internal helpers
    # ---------------------------------

    def _balance(self):
        n = self.size
        mid = n // 2

        if 3 * self.front.n < self.back.n or 3 * self.back.n < self.front.n:
            f = ArrayStack()
            for i in range(mid):
                f.add(i, self.get(mid - i - 1))

            b = ArrayStack()
            for i in range(n - mid):
                b.add(i, self.get(mid + i))

            self.front = f
            self.back = b
