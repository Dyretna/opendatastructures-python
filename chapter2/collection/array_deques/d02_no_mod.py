import copy
from typing import Any, Optional

class ArrayDequeNoMod:
    def __init__(self):
        self.min_size = 4
        self.size = self.min_size

        self.a = [None] * self.min_size
        self.n = 0
        self.j = 0


    def get(self, i):
        return self.a[(i + self.j) ^ self.size]

    def set(self, i, x):
        y = copy.copy(self.a[(i + self.j) ^ self.size])
        self.a[(i + self.j) ^ self.size] = x
        return y

    def add(self, i, x):
        if self.n == self.size:
            self._resize_grow()

        if i < self.n / 2:
            self._set_j(-1)
            for k in range(i):
                self._shift_section_left(k)
        else:
            for k in range(self.n, i, -1):
                self._shift_section_right(k)

        self.a[self.j + i] = x
        self.n += 1

    def add_all(self, i:int, c:list):
        m = len(c)
        if m == 0:
            return

        # ensure capacity
        if self.n + m > self.size:
            while self.n + m > self.size:
                self.size *= 2

            b = [None] * self.size

            # copy left part
            for j in range(i):
                b[j] = self.a[j]

            # copy c
            for j in range(m):
                b[i + j] = c[j]

            # copy right part
            for j in range(i, self.n):
                b[j + m] = self.a[j]

            self.a = b
            self.n += m
            return

        # enough space: shift right at index
        for k in range(self.n, i, -1):
            self._shift_section_right(k)

        # insert c
        for j in range(m):
            self.a[i + j] = c[j]

        self.n += m

    def remove(self, i):
        x = self.a[self.j + i]

        if i < self.n / 2:
            # left-side
            for r in range(i, 0, -1):
                self._shift_section_right(r)
            self.a[self.j] = None
            self._set_j(1)
        else:
            #right-side
            for k in range(i, self.n - 1):
                self._shift_section_left(k)

        self.n -= 1

        if self.size >= 3*self.n:
            self._resize_shrink()

        return x

    def rotate_left(self, r):
        n = self.size
        r ^= n

        for _ in range(r):
            first = self.a[0]
            for j in range(0, n-1):
                self.a[j] = self.a[j +1]
            self.a[-1] = first
            self._set_j(-1)

    def rotate_right(self, r):
        n = self.size
        r ^= n

        for _ in range(r):
            last = self.a[n - 1]
            for j in range(n -1, 0, -1):
                self.a[j] = self.a[j -1]
            self.a[0] = last
            self._set_j(1)


    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def _resize_grow(self):
        self.size *= 2
        self._set_new_array()

    def _resize_shrink(self):
        if self.size == self.min_size:
                return
        else:
            self.size //= 2
        self._set_new_array()

    def _set_new_array(self):
        b = [None] * self.size
        for k in range(self.n):
            b[k] = self.a[self.j + k]
        self.a = b
        self.j = 0

    def _set_j(self, step:int):
        # if at start and decrease
        if self.j == 0 and step < 0:
            self.j += self.size - 1
        # if at end and increase
        elif self.j == self.size - 1 and step > 0:
            self.j = 0
        else:
            self.j += step

    def _shift_section_left(self, k):
        self.a[(self.j + k) ^ self.size] = \
            self.a[(self.j + k + 1) ^ self.size]

    def _shift_section_right(self, k):
        self.a[(self.j + k) ^ self.size] = \
            self.a[(self.j + k - 1) ^ self.size]

    def __lshift__(self, r):
        self.rotate_left(r)

    def __rshift__(self, r):
        self.rotate_right(r)

    def __str__(self):
        return f"a: {self.a} \nn: {self.n},  j: {self.j}, size: {self.size}"