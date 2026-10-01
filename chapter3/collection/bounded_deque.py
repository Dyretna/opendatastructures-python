import copy
from typing import Any, Optional


class BDeque:
    def __init__(self, capacity: Optional[int] = 4):
        self.a = [None] * capacity
        self.capacity = capacity
        self.j = 0
        self.n = 0

    def size(self):
        return self.n

    def get(self, i:int):
        return self.a[self._get_idx(i)]

    def set(self, i:int, x:Any):
        old = self.a[self._get_idx(i)]
        self.a[self._get_idx(i)] = x
        return old

    def add(self, i:int, x:Any):
        if self.n == self.capacity:
            raise Exception("Block full")

        if i < self.n // 2:
            self.j = (self.j - 1) % self.capacity
            for k in range(i):
                self._shift_section_left(k)
        else:
            for k in range(self.n, i, -1):
                self._shift_section_right(k)

        self.a[self._get_idx(i)] = x
        self.n += 1

    def remove(self, i:int):
        x = self.a[self._get_idx(i)]

        if i < self.n // 2:
            for k in range(i, 0, -1):
                self._shift_section_right(k)
            self.a[self._get_idx(0)] = None
            self.j = (self.j + 1) % self.capacity
        else:
            for k in range(i, self.n - 1):
                self._shift_section_left(k)
            self.a[self._get_idx(self.n-1)] = None

        self.n -= 1
        return x

    def add_left(self, x:Any):
        if self.n == self.capacity:
            raise Exception("Block full")
        self.j = (self.j - 1) % self.capacity
        self.a[self.j] = x
        self.n += 1

    def add_right(self, x:Any):
        if self.n == self.capacity:
            raise Exception("Block full")
        self.a[(self.j + self.n) % self.capacity] = x
        self.n += 1

    def pop_left(self):
        x = self.a[self.j]
        self.j = (self.j + 1) % self.capacity
        self.n -= 1
        return x

    def pop_right(self):
        idx = (self.j + self.n - 1) % self.capacity
        x = self.a[idx]
        self.n -= 1
        return x

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def _get_idx(self, i:int):
        return (self.j + i) % self.capacity

    def _shift_section_left(self, i):
        self.a[self._get_idx(i)] = self.a[self._get_idx(i + 1)]

    def _shift_section_right(self, i):
        self.a[self._get_idx(i)] = self.a[self._get_idx(i - 1)]


    def __str__(self):
        return (
            f"a: {self.a}"
            f" \nn: {self.n}, "
            f" \nj: {self.j}, "
            f"capacity: {self.capacity}"
        )

