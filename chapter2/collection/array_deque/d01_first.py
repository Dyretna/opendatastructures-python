import copy
from typing import Any, Optional

class ArrayDeque:
    def __init__(self):
        self.a = []
        self.n = 0
        self.j = 0

    def get(self, i):
        return self.a[(i + self.j) % len(self.a)]

    def set(self, i, x):
        y = copy.copy(self.a[(i + self.j) % len(self.a)])
        self.a[(i + self.j) % len(self.a)] = x
        return y

    def add(self, i, x):
        if self.n == len(self.a):
            self.resize()

        if i < self.n / 2:
            self.j = (self.j-1) % len(self.a)
            for k in range(i):
                self._shift_section_left(k)
        else:
            for k in range(self.n, i, -1):
                self._shift_section_right(k)

        self.a[(self.j + i) % len(self.a)] = x
        self.n += 1

    def add_all(self, i:int, c:list):
        m = len(c)
        if m == 0:
            return

        # ensure capacity
        if self.n + m > len(self.a):
            new_capacity = max(1, 2*(self.n + m))
            b = [None] * new_capacity

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

        # enough space: rotate right
        for k in range(self.n, i, -1):
            self._shift_section_right(k)

        # insert c
        for j in range(m):
            self.a[i + j] = c[j]

        self.n += m

    def remove(self, i):
        x = self.a[(self.j + i) % len(self.a)]

        if i < self.n / 2:
            # left-side
            for r in range(i, 0, -1):
                self._shift_section_right(r)
            self.a[self.j] = None
            self.j = (self.j + 1) % len(self.a)
        else:
            #right-side
            for k in range(i, self.n - 1):
                self._shift_section_left(k)

        self.n -= 1

        if len(self.a) >= 3*self.n:
            self.resize()

        return x

    def rotate_left(self, r):
        n = len(self.a)
        r %= n

        for _ in range(r):
            first = self.a[0]
            for j in range(0, n-1):
                self.a[j] = self.a[j +1]
            self.a[-1] = first
            self.j = (self.j - 1) % len(self.a)

    def rotate_right(self, r):
        n = len(self.a)
        r %= n

        for _ in range(r):
            last = self.a[n - 1]
            for j in range(n -1, 0, -1):
                self.a[j] = self.a[j -1]
            self.a[0] = last
            self.j = (self.j + 1) % len(self.a)

    def resize(self):
        b = [None] * max(1, 2*self.n)
        for k in range(self.n):
            b[k] = self.a[(self.j + k) % len(self.a)]
        self.a = b
        self.j = 0

    # --------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------

    def __lshift__(self, r):
        self.rotate_left(r)

    def __rshift__(self, r):
        self.rotate_right(r)

    def _shift_section_left(self, k):
        self.a[(self.j + k) % len(self.a)] = \
            self.a[(self.j + k + 1) % len(self.a)]

    def _shift_section_right(self, k):
        self.a[(self.j + k) % len(self.a)] = \
            self.a[(self.j + k - 1) % len(self.a)]

    def __str__(self):
        return f"a: {self.a} \nn: {self.n}  j: {self.j}"