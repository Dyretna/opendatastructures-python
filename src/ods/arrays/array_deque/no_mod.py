from typing import Any

from .base import ArrayDequeBase


class NoModDeque(ArrayDequeBase):
    def __init__(self, min_size: int = 4):
        self.min_size = min_size
        self.a = [None] * self.min_size
        self.n = 0
        self.j = 0

    # -------------------------------------------------------
    # Abstract interface requirements
    # -------------------------------------------------------

    def get(self, i: int):
        self._index_bounds_check(i)
        return self.a[(self.j + i) & (len(self.a) - 1)]

    def set(self, i: int, x: Any):
        self._index_bounds_check(i)
        idx = (self.j + i) & (len(self.a) - 1)

        y = self.a[idx]
        self.a[idx] = x
        return y

    def add_first(self, x: Any):
        self.add(0, x)

    def add_last(self, x: Any):
        self.add(self.size, x)

    def remove_first(self):
        self.remove(0)

    def remove_last(self):
        self.remove(self.size)

    # -------------------------------------------------------
    # Public additions - operations with indexing, rotating...
    # -------------------------------------------------------

    def add(self, i: int, x: Any):
        self._index_bounds_check_adding(i)

        if self.n == len(self.a):
            self._resize_grow()

        if i < self.size / 2:
            self.j = (self.j - 1) & (len(self.a) - 1)
            for k in range(i):
                self._shift_section_left(k)
        else:
            for k in range(self.n, i, -1):
                self._shift_section_right(k)

        self.a[(self.j + i) & (len(self.a) - 1)] = x
        self.n += 1

    def add_all(self, i: int, c: list):
        """inserts elements of an iterable in order at index."""
        self._index_bounds_check_adding(i)

        m = len(c)
        if m == 0:
            return

        # ensure capacity
        if self.n + m > len(self.a):
            new_capacity = len(self.a)
            while new_capacity < self.n + m:
                new_capacity *= 2

            b = [None] * new_capacity

            # left side
            for k in range(i):
                b[k] = self.a[(self.j + k) & (len(self.a) - 1)]

            # inserted
            for k in range(m):
                b[i + k] = c[k]

            # right side
            for k in range(i, self.size):
                b[k + m] = self.a[(self.j + k) & (len(self.a) - 1)]

            self.a = b
            self.j = 0
            self.n += m
            return

        # enough space: rotate right
        for k in range(self.size, i, -1):
            self._shift_section_right(k)

        # insert c
        for k in range(m):
            self.a[(self.j + i + k) & (len(self.a) - 1)] = c[k]

        self.n += m

    def remove(self, i: int):
        self._index_bounds_check(i)

        x = self.a[(self.j + i) & (len(self.a) - 1)]

        if i < self.n / 2:
            # left-side
            for r in range(i, 0, -1):
                self._shift_section_right(r)
            self.a[self.j] = None
            self.j = (self.j + 1) & (len(self.a) - 1)
        else:
            # right-side
            for k in range(i, self.size - 1):
                self._shift_section_left(k)

        self.n -= 1

        if self.size <= len(self.a) // 3:
            self._resize_shrink()

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

    def _index_bounds_check(self, i: int):
        if not (0 <= i <= self.size - 1):
            raise IndexError("index not in range")

    def _index_bounds_check_adding(self, i: int):
        if not (0 <= i <= self.size):
            raise IndexError("index not in range")

    def _resize_grow(self):
        new_capacity = len(self.a) * 2
        self._set_new_array(new_capacity)

    def _resize_shrink(self):
        if len(self.a) == self.min_size:
            return
        else:
            new_capacity = len(self.a) // 2
        self._set_new_array(new_capacity)

    def _set_new_array(self, new_capacity: int):
        b = [None] * new_capacity

        for k in range(self.n):
            b[k] = self.a[(self.j + k) & (len(self.a) - 1)]

        self.a = b
        self.j = 0

    def _shift_section_left(self, i: int):
        self.a[(self.j + i) & len(self.a) - 1] = self.a[
            (self.j + i + 1) & (len(self.a) - 1)
        ]

    def _shift_section_right(self, i: int):
        self.a[(self.j + i) & len(self.a) - 1] = self.a[
            (self.j + i - 1) & (len(self.a) - 1)
        ]

    # --- Rotating ---
    def _rotate_left(self, r: int) -> None:
        if self.n <= 1:
            return

        r %= self.size
        mask = len(self.a) - 1

        for _ in range(r):
            first = self.a[self.j]

            # shift logical elements left (not empty slots)
            for k in range(self.size - 1):
                dst = (self.j + k) & mask
                src = (self.j + k + 1) & mask
                self.a[dst] = self.a[src]

            # write first at logical end
            last = (self.j + self.size - 1) & mask
            self.a[last] = first

    def _rotate_right(self, r: int) -> None:
        if self.size <= 1:
            return

        r %= self.size
        mask = len(self.a) - 1

        for _ in range(r):
            last = self.a[(self.j + self.size - 1) & mask]

            # shift logical elements right
            for k in range(self.size - 1, 0, -1):
                dst = (self.j + k) & mask
                src = (self.j + k - 1) & mask
                self.a[dst] = self.a[src]

            # write last to first
            self.a[self.j] = last

    def __lshift__(self, r: int):
        self._rotate_left(r)

    def __rshift__(self, r: int):
        self._rotate_right(r)

    def __str__(self):
        header = f" {__class__.__name__} ".center(50, "=")
        return header + "\n" + f"a: {self.a} \nn: {self.n}  j: {self.j}"
