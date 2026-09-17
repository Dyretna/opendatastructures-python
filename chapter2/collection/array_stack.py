from typing import Any
import copy


class ArrayStack:
    def __init__(self):
        self.a = []
        self.n = 0

    def get(self, i:int):
        return self.a[i]

    def set(self, i:int, x:Any) -> Any:
        y = copy.copy(self.a[i])
        self.a[i] = x
        return y

    def add(self, i:int, x:Any):
        if self.n == len(self.a):
            self.resize()

        # shift right: go backwards
        for j in range(self.n, i, -1):
            self.a[j] = self.a[j-1]

        self.a[i] = x
        self.n += 1

    def remove(self, i):
        x = self.a[i]

        # shift left
        for j in range(i, self.n - 1):
            self.a[j] = self.a[j + 1]

        # leave a None at the end
        self.a[self.n - 1] = None

        self.n -= 1

        if len(self.a) >= 3 * self.n:
            self.resize()

        return x

    def resize(self):
        # ensure at least size 1
        new_capacity = max(1, 2*self.n)
        b = [None] * new_capacity
        for i in range(self.n):
            b[i] = self.a[i]

        self.a = b

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

        # enough space: shift right
        # backwards to not overwrite data
        for j in range(self.n - 1, i - 1, -1):
            self.a[j + m] = self.a[j]

        # insert c
        for j in range(m):
            self.a[i + j] = c[j]

        self.n += m

