"""
This is a work in progress, below i am working out an
idea.

We can see in the exercise description, that we should be able to
shift elements to both directions when adding or removing. The core
conceptual problem is, if we are to shift elements to the left how
do we grow extra space, when the blocks in the rootish structure
grows towards the end?

While the next exercise (2.10) hints towards a SEL-like solution,
using bounded deques, 2.9 has no such hints, therefore the
datastructures from this chapter should be enough.

while i thought i had a solution and moved on the next, this was
really not the case - i had just copied the original version, tried
something, and forgot about it.

pondering the conceptual problem here, with having blocks that increases
in size by one, and having to shift to the left... stacks wont help,
queues wont help, and deques won't either...

the closest thing must be the DualArrayDeque.. with something similar,
we could build an hourglass-like rootish structure as below:

    front_blocks

    [4,4,4,4]
    [3,3,3]
    [2,2]
    [1]

    -- centre --

    [1]
    [2,2]
    [3,3,3]
    [4,4,4,4]

    back_blocks

That seems to be like that way to go forward, it would be easy to extend
with new blocks at both ends, so i will try to go further with this idea.
The new problem will be the index to block translation in the method:

    ```
    def i2b(self, i: int):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))
    ```

and i hit another brick wall. to be continued...

"""

from math import ceil, sqrt
from typing import Any

from ..array_stack import ArrayStack


class ImprovedRAS:
    """
    An implementation of a RootishArrayStack that:
    has only O(√n) wasted space, but that can perform
    add(i, x) and remove(i, x) operations in

        *O(1 + min{i, n - i})*

    time.

    """

    def __init__(self):
        self.n = 0
        self.front_blocks = ArrayStack()
        self.back_blocks = ArrayStack()

    @property
    def size(self):
        return self.front_blocks.n + self.back_blocks.n

    def is_empty(self):
        return self.size == 0

    def i2b(self, i: int):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def get(self, i):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        b = self.i2b(i)
        # j is the index inside block b
        j = i - b * (b + 1) // 2
        return self.blocks.get(b)[j]

    def set(self, i: int, x: Any):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        b = self.i2b(i)
        j = i - b * (b + 1) // 2
        old = self.blocks.get(b)[j]
        self.blocks.get(b)[j] = x
        return old

    def add(self, i: int, x: Any):
        self._index_bounds_check_adding(i)

        ...

    def remove(self, i: int):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        ...

    # ---------------------------------------------------
    # internal helpers
    # ---------------------------------------------------

    def _index_bounds_check(self, i: int):
        if not (0 <= i <= self.size - 1):
            raise IndexError("index not in range")

    def _index_bounds_check_adding(self, i: int):
        if not (0 <= i <= self.size):
            raise IndexError("index not in range")

    def _grow(self):
        # add a new block of size r+1 (filled with None)
        r = self.blocks.size
        new_block = [None] * (r + 1)
        # append at the end of blocks
        self.blocks.add(self.blocks.size, new_block)

    def _shrink(self):
        r = self.blocks.size

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
        # out.append(f"logical blocks     : {self.blocks.n}")
        # out.append(f"reserved blocks    : {len(self.blocks.a) - self.blocks.n}\n")

        for i in range(self.blocks.n):
            block = self.blocks.get(i)
            b_start = i * (i + 1) // 2
            remaining_elements = max(0, self.n - b_start)
            visible_count = min(len(block), remaining_elements)

            display = block[:visible_count] + [None] * (len(block) - visible_count)
            out.append(f"block {i:^3}: {display}")

        return "\n".join(out)
