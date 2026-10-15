from typing import Any

from .base import ArrayDequeBase


class NoModDeque(ArrayDequeBase):
    def __init__(self, min_size: int = 4):
        self.min_size = min_size
        self.a = [None] * self.min_size
        self.n = 0
        self.j = 0

    # -------------------------------------------------------
    # Abstract interface requirements - override with caret!
    # -------------------------------------------------------

    def get(self, i: int):
        if i + self.j >= self.size:
            return self.a[(i + self.j) ^ len(self.a)]
        else:
            return self.a[i + self.j]

    def set(self, i: int, x: Any):
        if i + self.j >= self.size:
            y = self.a[(i + self.j) ^ len(self.a)]
            self.a[(i + self.j) ^ self.size] = x
        else:
            y = self.a[i + self.j]
            self.a[i + self.j] = x
        return y

    # -------------------------------------------------------
    # Public additions - operations with indexing, rotating...
    # -------------------------------------------------------

    def add(self, i: int, x: Any):
        if self.n == len(self.a):
            self._resize_grow()

        if i < self.size / 2:
            self.j = self._set_j(-1)
            for k in range(i):
                self._shift_section_left(k)
        else:
            for k in range(self.n, i, -1):
                self._shift_section_right(k)

        self.a[(i + self.j) ^ len(self.a) - len(self.a)] = x
        self.n += 1

    def add_all(self, i: int, c: list):
        """inserts elements of an iterable in order at index."""
        m = len(c)
        if m == 0:
            return

        # ensure capacity
        new_capacity = max(4, len(self.a))
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
        x = self.a[(i + self.j) ^ len(self.a) - len(self.a)]

        if i < self.n / 2:
            # left-side
            for r in range(i, 0, -1):
                self._shift_section_right(r)
            self.a[self.j] = None
            self.j = self._set_j(1)
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
            b[k] = self.a[self.j + k]
        self.a = b
        self.j = 0

    def _set_j(self, step: int):
        # if at start and decrease
        if self.j == 0 and step < 0:
            self.j += self.size - 1
        # if at end and increase
        elif self.j == self.size - 1 and step > 0:
            self.j = 0
        else:
            self.j += step

    def _shift_section_left(self, k: int):
        self.a[(self.j + k) ^ len(self.a)] = self.a[(self.j + k + 1) ^ len(self.a)]

    def _shift_section_right(self, k: int):
        self.a[(self.j + k) ^ len(self.a)] = self.a[(self.j + k - 1) ^ len(self.a)]

    # --- Rotating ---

    def _rotate_left(self, r: int) -> None:
        r ^= len(self.a)

        for _ in range(r):
            first = self.a[0]
            for j in range(0, len(self.a) - 1):
                self.a[j] = self.a[j + 1]
            self.a[-1] = first
            self.j = self._set_j(-1)

    def _rotate_right(self, r: int) -> None:
        r ^= len(self.a)

        for _ in range(r):
            last = self.a[len(self.a) - 1]
            for j in range(len(self.a) - 1, 0, -1):
                self.a[j] = self.a[j - 1]
            self.a[0] = last
            self.j = self._set_j(1)

    def __lshift__(self, r: int):
        self._rotate_left(r)

    def __rshift__(self, r: int):
        self._rotate_right(r)

    def __str__(self):
        header = f" {__class__.__name__} ".center(50, "=")
        return header + "\n" + f"a: {self.a} \nn: {self.n}  j: {self.j}"
