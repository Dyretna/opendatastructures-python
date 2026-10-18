from math import ceil, sqrt
from typing import Any


class EvenFurtherImprovedRAS:
    """
    An implementation of a RootishArrayStack that:
    has only O(√n) wasted space, but that can perform
    add(i, x) and remove(i, x) operations in

        *O(1 + min{i, √n, n - i})*

    time.

    """

    def __init__(self):
        self.n = 0
        pass

    @property
    def size(self):
        return self.n

    def is_empty(self):
        return self.n == 0

    def i2b(self, i: int):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def get(self, i):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        b = self.i2b(i)
        # j is the index inside block b
        j = i - b * (b + 1) // 2
        return self.blocks.get(b).get(j)

    def set(self, i: int, x: Any):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        b = self.i2b(i)
        j = i - b * (b + 1) // 2
        old = self.blocks.get(b).get(j)
        self.blocks.get(b).set(j, x)
        return old

    def append(self, x: Any):
        pass

    def add(self, i: int, x: Any):
        pass

    def remove(self, i: int):
        pass

    # ---------------------------------------------------
    # internal helpers
    # ---------------------------------------------------

    # --- adders ---
    def _add_from_left(self, i: int):
        pass

    def _add_from_middle(self):
        pass

    def _add_from_right(self):
        pass

    # --- removers ---
    def _remove_from_left(self):
        pass

    def _remove_from_middle(self):
        pass

    def _remove_from_right(self):
        pass

    # ----------------------------------------------------

    def _index_bounds_check(self, i: int):
        if not (0 <= i <= self.size - 1):
            raise IndexError("index not in range")

    def _index_bounds_check_adding(self, i: int):
        if not (0 <= i <= self.size):
            raise IndexError("index not in range")

    def _initialize_first_block(self):
        pass

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
        pass

    def _spread(self, b: int) -> None:
        pass

    def _gather(self, b: int) -> None:
        pass

    def _shrink(self):
        pass

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
            visible_count = min(block.size, remaining_elements)

            display = [block.get(j) for j in range(visible_count)]
            display += [None] * (block.capacity - visible_count)
            out.append(f"block {i:^3}: {display}")

        return "\n".join(out)
