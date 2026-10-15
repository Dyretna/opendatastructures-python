from typing import Any

from .base import ArrayDequeBase


class ArrayDeque(ArrayDequeBase):
    @property
    def capacity(self):
        return len(self.a)

    def add(self, i: int, x: Any):
        if self.n == self.capacity:
            self._resize()

        if i < self.size / 2:
            self.j = self._get_mod_idx(-1)
            for k in range(i):
                self._shift_section_left(k)
        else:
            for k in range(self.n, i, -1):
                self._shift_section_right(k)

        self.a[self._get_mod_idx(i)] = x
        self.n += 1

    def add_all(self, i: int, c: list):
        """inserts elements of an iterable in order at index."""
        m = len(c)
        if m == 0:
            return

        # ensure capacity
        new_capacity = max(1, self.capacity)
        if self.n + m > new_capacity:
            while self.n + m > new_capacity:
                new_capacity *= 2

            b = [None] * new_capacity

            # copy left part
            for j in range(i):
                b[j] = self.a[j]

            # copy c
            for j in range(m):
                b[i + j] = c[j]

            # copy right part
            for j in range(i, self.size):
                b[j + m] = self.a[j]

            self.a = b
            self.n += m
            return

        # enough space: rotate right
        for k in range(self.size, i, -1):
            self._shift_section_right(k)

        # insert c
        for j in range(m):
            self.a[i + j] = c[j]

        self.n += m

    def remove(self, i: int):
        x = self.a[self._get_mod_idx(i)]

        if i < self.n / 2:
            # left-side
            for r in range(i, 0, -1):
                self._shift_section_right(r)
            self.a[self.j] = None
            self.j = self._get_mod_idx(1)
        else:
            # right-side
            for k in range(i, self.size - 1):
                self._shift_section_left(k)

        self.n -= 1
        if self.size <= self.capacity // 3:
            self._resize()

        return x

    def rotate(self, r: int):
        if r == 0:
            return
        elif r < 0:
            self._rotate_left(abs(r))
            return
        elif r > 0:
            self._rotate_right(r)
            return

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def _get_mod_idx(self, i: int) -> int:
        return (i + self.j) % len(self.a)

    def _shift_section_left(self, i: int) -> None:
        self.a[self._get_mod_idx(i)] = self.a[self._get_mod_idx(i + 1)]

    def _shift_section_right(self, i: int) -> None:
        self.a[self._get_mod_idx(i)] = self.a[self._get_mod_idx(i - 1)]

    def _resize(self) -> None:
        b = [None] * max(1, 2 * self.capacity)
        for k in range(self.n):
            b[k] = self.get(self._get_mod_idx(k))
        self.a = b
        self.j = 0

    def _rotate_left(self, r: int) -> None:
        r %= self.capacity

        for _ in range(r):
            first = self.a[0]
            for j in range(0, self.capacity - 1):
                self.a[j] = self.a[j + 1]
            self.a[-1] = first
            self.j = self._get_mod_idx(-1)

    def _rotate_right(self, r: int) -> None:
        r %= self.capacity

        for _ in range(r):
            last = self.a[self.capacity - 1]
            for j in range(self.capacity - 1, 0, -1):
                self.a[j] = self.a[j - 1]
            self.a[0] = last
            self.j = self._get_mod_idx(1)

    def __lshift__(self, r: int):
        self._rotate_left(r)

    def __rshift__(self, r: int):
        self._rotate_right(r)

    def __str__(self):
        header = f" {__class__.__name__} ".center(50, "=")
        return header + "\n" + f"a: {self.a} \nn: {self.n}  j: {self.j}"
