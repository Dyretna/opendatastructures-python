from math import ceil, sqrt
from typing import Any

from ..array_deque import BoundedDeque
from ..array_stack import ArrayStack


class FurtherImprovedRAS:
    """
    An implementation of a RootishArrayStack that:
    has only O(√n) wasted space, but that can perform
    add(i, x) and remove(i, x) operations in

        *O(1 + min{√n, n - i})*

    time.

    """

    def __init__(self):
        self.n = 0
        self.blocks: ArrayStack[BoundedDeque | None] = ArrayStack()
        self._initialize_first_block()  # insert bdeque with cap = 1

    @property
    def size(self):
        return self.n

    def is_empty(self):
        return self.n == 0

    def i2b(self, i: int):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def get(self, i):
        b = self.i2b(i)
        # j is the index inside block b
        j = i - b * (b + 1) // 2
        return self.blocks.get(b).get(j)

    def set(self, i: int, x: Any):
        b = self.i2b(i)
        j = i - b * (b + 1) // 2
        old = self.blocks.get(b).get(j)
        self.blocks.get(b).set(j, x)
        return old

    def append(self, x: Any):
        self._ensure_capacity()
        block: BoundedDeque = self.blocks.get(self.blocks.size - 1)
        block.add_last(x)
        self.n += 1

    def add(self, i: int, x: Any):
        # if we add to end - simply append
        if i == self.n:
            self.append(x)
            return

        self._ensure_capacity()

        b = self.i2b(i)
        block: BoundedDeque = self.blocks.get(b)

        if block.size == block.capacity:
            self._spread(b)

        if block.size == block.capacity:
            self._grow()

        j = i - b * (b + 1) // 2
        self.blocks.get(b).add(j, x)
        self.n += 1

    def remove(self, i: int):
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
        self.blocks.a = [BoundedDeque(capacity=1)]

    def _ensure_capacity(self):
        """
        Ensure there is room for one more element:
        while total capacity < n+1, grow
        """
        r = self.blocks.size
        while r * (r + 1) // 2 < self.n + 1:
            self._grow()
            r = self.blocks.size

    def _grow(self):
        # add a new block of size r+1 (filled with None)
        r = self.blocks.size
        new_block = BoundedDeque(capacity=r + 1)
        self.blocks.add(self.blocks.size, new_block)

    def _spread(self, b: int) -> None:
        for i in range(self.blocks.size - 1, b, -1):
            source: BoundedDeque = self.blocks.get(i - 1)
            target: BoundedDeque = self.blocks.get(i)

            if source.size == 0:
                continue

            if target.size < target.capacity:
                target.add_first(source.remove_last())
            else:
                # fallback if full
                break

    def _gather(self, b: int) -> None:
        for i in range(b, self.blocks.size - 1):
            if self.blocks.get(i + 1).size == 0:
                continue

            elem = self.blocks.get(i + 1).remove_first()
            self.blocks.get(i).add_last(elem)
        self._shrink()

    def _shrink(self):
        r = self.blocks.size

        while r > 0 and ((r - 1) * (r - 2)) // 2 >= self.n:
            self.blocks.a[r - 1] = None
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
        out.append(f"logical blocks     : {self.blocks.size}")
        out.append(f"reserved blocks    : {len(self.blocks.a) - self.blocks.size}\n")

        for i in range(self.blocks.size):
            block = self.blocks.get(i)
            b_start = i * (i + 1) // 2
            remaining_elements = max(0, self.n - b_start)
            visible_count = min(block.size, remaining_elements)

            display = [block.get(j) for j in range(visible_count)]
            display += [None] * (block.capacity - visible_count)
            out.append(f"block {i:^3}: {display}")

        return "\n".join(out)
