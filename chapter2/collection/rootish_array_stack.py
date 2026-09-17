from math import ceil, sqrt
import copy

from .array_stack import ArrayStack

class RootishArrayStack:
    def __init__(self):
        # number of elements stored
        self.n = 0
        # stack of blocks; each block is a Python list
        self.blocks = ArrayStack()

    def i2b(self, i):
        # compute block index b that contains element at list index i (0-based)
        # solve (b+1)(b+2)/2 >= i+1 and take the ceiling of the positive root
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def get(self, i):
        # bounds check
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

        # increase element count and shift elements right to make space
        self.n += 1
        for j in range(self.n - 1, i, -1):
            self.set(j, self.get(j - 1))
        self.set(i, x)

    def grow(self):
        # add a new block of size r+1 (filled with None)
        r = self.blocks.n
        new_block = [None] * (r + 1)
        # append at the end of blocks
        self.blocks.add(self.blocks.n, new_block)

    def remove(self, i):
        # remove and return element at index i
        if i < 0 or i >= self.n:
            raise IndexError("index out of range")
        x = self.get(i)

        # shift elements left to fill the gap
        for j in range(i, self.n - 1):
            self.set(j, self.get(j + 1))

        # clear the now-unused last slot to avoid duplicated trailing values
        last_index = self.n - 1
        b_last = self.i2b(last_index)
        j_last = last_index - b_last * (b_last + 1) // 2
        self.blocks.get(b_last)[j_last] = None

        # decrement element count
        self.n -= 1

        # shrink blocks if there are too many
        r = self.blocks.n
        while r > 0 and (r - 2) * (r - 1) // 2 >= self.n:
            self.blocks.remove(self.blocks.n - 1)
            r -= 1

        return x

    def shrink(self):
        # optional separate shrink method:
        # remove trailing blocks while capacity is excessive
        r = self.blocks.n
        while r > 0 and (r - 2) * (r - 1) // 2 >= self.n:
            self.blocks.remove(self.blocks.n - 1)
            r -= 1
