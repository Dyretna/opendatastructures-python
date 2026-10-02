from math import ceil, sqrt
import copy
from typing import Any

from ..array_stack import ArrayStack

class RootishArrayStack:
    def __init__(self):
        # number of elements stored
        self.n = 0
        # stack of blocks; each block is a Python list
        self.blocks = ArrayStack()

    def i2b(self, i:int):
        # compute block index b that contains element at list index i (0-based)
        # solve (b+1)(b+2)/2 >= i+1 and take the ceiling of the positive root
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def get(self, i:int):
        b = self.i2b(i)
        # j is the index inside block b
        j = i - b * (b + 1) // 2
        return self.blocks.get(b)[j]

    def set(self, i:int, x:Any):
        b = self.i2b(i)
        j = i - b * (b + 1) // 2
        # return a shallow copy of the old value, then replace it
        y = copy.copy(self.blocks.get(b)[j])
        self.blocks.get(b)[j] = x
        return y

    def add(self, i:int, x:Any):
        # ensure there is room for one more element:
        # while total capacity < n+1, grow
        r = self.blocks.n
        if r * (r + 1) / 2 < self.n + 1:
            self._grow()

        # increase element count and shift elements right to make space
        self.n += 1
        for j in range(self.n - 1, i, -1):
            self.set(j, self.get(j - 1))
        self.set(i, x)

    def remove(self, i:int):
        x = self.get(i)

        # shift elements left to fill the gap
        for j in range(i, self.n - 1):
            self.set(j, self.get(j + 1))

        # decrement element count
        self.n -= 1
        self._shrink()

        return x

    # ---------------------------------------------------
    # internal helpers
    # ---------------------------------------------------

    def _grow(self):
        # add a new block of size n + 1 (filled with None)
        new_block = [None] * (self.blocks.n + 1)
        # append at the end of blocks
        self.blocks.add(self.blocks.n, new_block)

    def _shrink(self):
        # optional separate shrink method:
        # remove trailing blocks while capacity is excessive
        r = self.blocks.n
        while r > 0 and ((r - 1) * r) // 2 >= self.n:
            self.blocks.a[r - 1] = None
            self.blocks.remove(r - 1)
            r -= 1

    def __str__(self):
        import re
        out = []
        out.append("\n=== Original RootishArrayStack ===")
        out.append(f"elements           : {self.n}")
        out.append(f"logical blocks     : {self.blocks.n}")
        out.append(f"reserved blocks    : {len(self.blocks.a) - self.blocks.n}\n")

        blocks = "\n".join(
            [f"block {i:^3}: {block}" for i, block in enumerate(self.blocks.a)]
        )
        out.append(blocks)
        return "\n".join(out)