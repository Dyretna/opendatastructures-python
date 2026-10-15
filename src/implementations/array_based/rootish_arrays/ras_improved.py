from math import ceil, sqrt
from typing import Any

from ..array_stack import ArrayStack


class ImprovedRAS:
    """
    An implementation of a RootishArrayStack that:
    has only O(√n) wasted space, but that can perform
    add(i, x) and remove(i, x) operations in

        *O(1 + min{i , n - i})*

    time.

    """

    def __init__(self):
        self.n = 0
        self.blocks = ArrayStack()

    def i2b(self, i: int):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def get(self, i):
        b = self.i2b(i)
        # j is the index inside block b
        j = i - b * (b + 1) // 2
        return self.blocks.get(b)[j]

    def set(self, i: int, x: Any):
        b = self.i2b(i)
        j = i - b * (b + 1) // 2
        old = self.blocks.get(b)[j]
        self.blocks.get(b)[j] = x
        return old

    def add(self, i: int, x: Any):
        # ensure there is room for one more element:
        # while total capacity < n+1, grow
        r = self.blocks.n

        while r * (r + 1) // 2 < self.n + 1:
            self._grow()
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

    def remove(self, i: int):
        x = self.get(i)

        if i < self.n // 2:
            # shift left side downward
            for j in range(i, 0, -1):
                self.set(j, self.get(j - 1))
        else:
            # shift right side upward
            for j in range(i, self.n - 1):
                self.set(j, self.get(j + 1))

        self.n -= 1
        self._shrink()

        return x

    # ---------------------------------------------------
    # internal helpers
    # ---------------------------------------------------

    def _grow(self):
        # add a new block of size r+1 (filled with None)
        r = self.blocks.n
        new_block = [None] * (r + 1)
        # append at the end of blocks
        self.blocks.add(self.blocks.n, new_block)

    def _shrink(self):
        r = self.blocks.n

        while r > 0 and ((r - 1) * (r - 2)) // 2 >= self.n:
            self.blocks.a[r - 1] = None
            self.blocks.remove(r - 1)
            r -= 1

    def __str__(self):
        """Displays blocks with zombie values masked as None.

        Keeps implementation faithful to pseudocode and optimized:
        - Zombie values not cleared in remove() (left for natural overwrite)
        - Same block lists reused (no new allocations on add)
        - Output shows only visible elements within current n
        """

        out = []
        out.append("\n=== Improved RootishArrayStack ===")
        out.append(f"elements           : {self.n}")
        out.append(f"logical blocks     : {self.blocks.n}")
        out.append(f"reserved blocks    : {len(self.blocks.a) - self.blocks.n}\n")

        for i in range(self.blocks.n):
            block = self.blocks.get(i)
            b_start = i * (i + 1) // 2
            remaining_elements = max(0, self.n - b_start)
            visible_count = min(len(block), remaining_elements)

            display = block[:visible_count] + [None] * (len(block) - visible_count)
            out.append(f"block {i:^3}: {display}")

        return "\n".join(out)
