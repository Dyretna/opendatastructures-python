from math import ceil, sqrt
import copy

from ..array_stack import ArrayStack

class FurtherImprovedRAS:
    def __init__(self):
        self.n = 0
        self.blocks = ArrayStack()

    def i2b(self, i):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def get(self, i):
        if i < 0 or i >= self.n:
            raise IndexError("index out of range")
        b = self.i2b(i)
        # j is the index inside block b
        j = i - b * (b + 1) // 2
        return self.blocks.get(b)[j]

    def set(self, i, x):
        # bounds check
        if i < 0 or i >= self.n:
            raise IndexError("index out of range")
        b = self.i2b(i)
        j = i - b * (b + 1) // 2
        # return a shallow copy of the old value, then replace it
        old = copy.copy(self.blocks.get(b)[j])
        self.blocks.get(b)[j] = x
        return old

    def add(self, i, x):
        # insert x at index i (0 <= i <= n)
        if i < 0 or i > self.n:
            raise IndexError("index out of range")

        # ensure there is room for one more element:
        # while total capacity < n+1, grow
        r = self.blocks.n
        while r * (r + 1) // 2 < self.n + 1:
            self.grow()
            r = self.blocks.n

        self.n += 1

        if i < self.n // 2:
            # shift elements left side upward
            for j in range(0, i):
                self.set(j, self.get(j))
            for j in range(i, 0, -1):
                self.set(j, self.get(j - 1))
            self.set(i, x)
        else:
            # shift right side downward
            for j in range(self.n - 1, i, -1):
                self.set(j, self.get(j - 1))
            self.set(i, x)

    def remove(self, i):
        # remove and return element at index i
        if i < 0 or i >= self.n:
            raise IndexError("index out of range")

        x = self.get(i)

        if i < self.n // 2:
            # shift left side downward
            for j in range(i, 0, -1):
                self.set(j, self.get(j - 1))
        else:
            # shift right side upward
            for j in range(i, self.n -1):
                self.set(j, self.get(j + 1))

        self.n -= 1
        self.shrink()

        return x

    def grow(self):
        # add a new block of size r+1 (filled with None)
        r = self.blocks.n
        new_block = [None] * (r + 1)
        # append at the end of blocks
        self.blocks.add(self.blocks.n, new_block)

    def shrink(self):
        r = self.blocks.n
        while r > 0 and (r - 2) * (r - 1) // 2 >= self.n:
            self.blocks.remove(self.blocks.n - 1)
            r -= 1


    def __str__(self):
        return "\n".join(
            [f"{i:^3} {block}" for i, block in enumerate(self.blocks.a)]
        )