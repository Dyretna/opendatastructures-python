from math import ceil, sqrt
import copy
from typing import Any

from ..array_stack import ArrayStack
from .bounded_deque import BDeque


class FurtherImprovedRAS:
    def __init__(self):
        self.n = 0
        self.blocks:ArrayStack[BDeque | None] = ArrayStack()
        self._initialize_first_block() # insert bdeque with cap = 1

    def i2b(self, i:int):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def get(self, i):
        b = self.i2b(i)
        # j is the index inside block b
        j = i - b * (b + 1) // 2
        return self.blocks.get(b).get(j)

    def set(self, i:int, x:Any):
        b = self.i2b(i)
        j = i - b * (b + 1) // 2
        old = self.blocks.get(b).get(j)
        self.blocks.get(b).set(j, x)
        return old

    def append(self, x:Any):
        self._ensure_capacity()
        block: BDeque = self.blocks.get(self.blocks.n - 1)
        block.add_right(x)
        self.n += 1

    def add(self, i:int, x:Any):
        # if we add to end - simply append
        if i == self.n:
            self.append(x)
            return

        self._ensure_capacity()

        b = self.i2b(i)
        block: BDeque = self.blocks.get(b)

        if block.size() == block.capacity:
            self._spread(b)

        if block.size() == block.capacity:
            self._grow()

        j = i - b * (b + 1) // 2
        self.blocks.get(b).add(j, x)
        self.n += 1

    def remove(self, i:int):
        x = self.get(i)

        b = self.i2b(i)
        j = i - b * (b + 1) // 2
        self.blocks.get(b).remove(j)

        self.n -= 1
        self._gather(b)

        return x

    # ---------------------------------------------------
    # internal helpers
    # ---------------------------------------------------

    def _initialize_first_block(self):
        self.blocks.a = [BDeque(capacity=1)]

    def _ensure_capacity(self):
        """
        Ensure there is room for one more element:
        while total capacity < n+1, grow
        """
        r = self.blocks.n
        while r * (r + 1) // 2 < self.n + 1:
            self._grow()
            r = self.blocks.n

    def _grow(self):
        # add a new block of size r+1 (filled with None)
        r = self.blocks.n
        new_block = BDeque(capacity=r + 1)
        self.blocks.add(self.blocks.n, new_block)

    def _spread(self, b:int) -> None:

        for i in range(self.blocks.n - 1, b, -1):
            source:BDeque = self.blocks.get(i - 1)
            target:BDeque = self.blocks.get(i)

            if source.size() == 0:
                continue

            if target.size() < target.capacity:
                target.add_left(source.pop_right())
            else:
                # fallback if full
                break

    def _gather(self, b:int) -> None:
        for i in range(b, self.blocks.n -1):
            elem = self.blocks.get(i + 1).pop_left()
            self.blocks.get(i).add_right(elem)
        self._shrink()

    def _shrink(self):
        # optional separate shrink method:
        # remove trailing blocks while capacity is excessive
        r = self.blocks.n

        while r > 0 and ((r-1) * (r-2)) // 2 >= self.n:
            self.blocks.a[r-1] = None
            self.blocks.remove(r - 1)
            r -= 1

    def __str__(self):
        """Displays blocks showing only logical elements within current n.

        Uses get() to retrieve elements instead of reading backing array
        directly, avoiding zombie values from removed elements.

        Shows:
        - elements count
        - logical blocks count
        - reserved blocks count (backing array capacity minus used blocks)
        - Each block with its visible elements (zombies masked as None)
        """

        out = []
        out.append("\n=== Further Improved RootishArrayStack ===")
        out.append(f"elements           : {self.n}")
        out.append(f"logical blocks     : {self.blocks.n}")
        out.append(f"reserved blocks    : {len(self.blocks.a) - self.blocks.n}\n")

        for i in range(self.blocks.n):
            block = self.blocks.get(i)
            b_start = i * (i + 1) // 2
            remaining_elements = max(0, self.n - b_start)
            visible_count = min(block.size(), remaining_elements)

            display = [block.get(j) for j in range(visible_count)]
            display += [None] * (block.capacity - visible_count)
            out.append(f"block {i:^3}: {display}")

        return "\n".join(out)