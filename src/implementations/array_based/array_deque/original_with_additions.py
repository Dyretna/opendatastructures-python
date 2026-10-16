from typing import Any

from .base import ArrayDequeBase


class ArrayDeque(ArrayDequeBase):
    # ------------------------------------------------------
    # Abstract interface requirements
    # - add_first(), add_last(), remove_first(), remove_last()
    # in parent class
    # ------------------------------------------------------

    def get(self, i: int):
        self._index_bounds_check(i)
        return self.a[(self.j + i) % len(self.a)]

    def set(self, i: int, x: Any):
        self._index_bounds_check(i)
        y = self.a[(self.j + i) % len(self.a)]
        self.a[(self.j + i) % len(self.a)] = x
        return y

    # ------------------------------------------------------
    # additional Deque operations - indexing, rotation, etc..
    # -----------------------------------------------------

    @property
    def capacity(self):
        return len(self.a)

    def add(self, i: int, x: Any):
        self._index_bounds_check_adding(i)

        if self.n == self.capacity:
            self._resize_grow()

        if i < self.size / 2:
            self.j = (self.j - 1) % self.capacity
            for k in range(i):
                self._shift_section_left(k)
        else:
            for k in range(self.n, i, -1):
                self._shift_section_right(k)

        self.a[(self.j + i) % self.capacity] = x
        self.n += 1

    def add_all(self, i: int, c: list):
        """inserts elements of an iterable in order at index."""
        self._index_bounds_check_adding(i)

        m = len(c)
        if m == 0:
            return

        # ensure capacity
        if self.n + m > self.capacity:
            new_capacity = self.capacity
            while new_capacity < self.n + m:
                new_capacity *= 2

            b = [None] * new_capacity

            # Left side
            for k in range(i):
                b[k] = self.a[(self.j + k) % self.capacity]

            # insertion
            for k in range(m):
                b[i + k] = c[k]

            # Right side
            for k in range(i, self.size):
                b[k + m] = self.a[(self.j + k) % self.capacity]

            self.a = b
            self.j = 0
            self.n += m
            return

        # enough space: shift right
        for k in range(self.size, i, -1):
            self._shift_section_right(k)

        # insert valies
        for j in range(m):
            self.a[i + j] = c[j]

        self.n += m

    def remove(self, i: int):
        self._index_bounds_check(i)

        x = self.a[(self.j + i) % self.capacity]

        if i < self.n / 2:
            # left-side
            for r in range(i, 0, -1):
                self._shift_section_right(r)

            self.a[self.j] = None
            self.j = (self.j + 1) % self.capacity
        else:
            # right-side
            for k in range(i, self.size - 1):
                self._shift_section_left(k)

            self.a[(self.j + self.n - 1) % self.capacity] = None

        self.n -= 1
        if self.capacity > 4 and self.capacity >= 3 * self.size:
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
        if self.capacity == 4:
            return
        else:
            new_capacity = len(self.a) // 2
        self._set_new_array(new_capacity)

    def _set_new_array(self, new_capacity: int):
        b = [None] * new_capacity
        for k in range(self.size):
            b[k] = self.a[(self.j + k) % self.capacity]
        self.a = b
        self.j = 0

    def _shift_section_left(self, i: int) -> None:
        self.a[(self.j + i) % len(self.a)] = self.a[(self.j + i + 1) % len(self.a)]

    def _shift_section_right(self, i: int) -> None:
        self.a[(self.j + i) % len(self.a)] = self.a[(self.j + i - 1) % len(self.a)]

    # --- Rotating ---
    def _rotate_left(self, r: int) -> None:
        if self.n <= 1:
            return

        r %= self.size

        for _ in range(r):
            first = self.a[self.j]

            # shift logical elements left (not empty slots)
            for k in range(self.size - 1):
                dst = (self.j + k) % self.capacity
                src = (self.j + k + 1) % self.capacity
                self.a[dst] = self.a[src]

            # write first at logical end
            last = (self.j + self.size - 1) % self.capacity
            self.a[last] = first

    def _rotate_right(self, r: int) -> None:
        if self.size <= 1:
            return

        r %= self.size

        for _ in range(r):
            last = self.a[(self.j + self.size - 1) % self.capacity]

            # shift logical elements right
            for k in range(self.size - 1, 0, -1):
                dst = (self.j + k) % self.capacity
                src = (self.j + k - 1) % self.capacity
                self.a[dst] = self.a[src]

            # write last to first
            self.a[self.j] = last

    def __lshift__(self, r: int):
        self._rotate_left(r)

    def __rshift__(self, r: int):
        self._rotate_right(r)

    def __str__(self):
        out = [f" {__class__.__name__} ".center(50, "=")]
        out.append(f"a : {self.a}")
        out.append(f"j : {self.j}")
        out.append(f"size : {self.size}")
        return "\n" + "\n".join(out)
