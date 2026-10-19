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

    front_blocks (but inverted, back to back)

    [1,2,3,4]
    [6,5,7]
    [8,9]
    [10]

    -- centre --

    [11]
    [12,13]
    [14,15,16]
    [17,18,19,20]

    back_blocks

That seems to be like that way to go forward, it would be easy to extend
with new blocks at both ends, so i will try to go further with this idea.
The new problem will be the index to block translation in the method:

    ```
    def i2b(self, i: int):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))
    ```

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
        self.front_n = 0
        self.front = ArrayStack()
        self.back = ArrayStack()

    @property
    def size(self):
        return self.n

    @property
    def total_blocks(self):
        return self.front.size + self.back.size

    def is_empty(self):
        return self.size == 0

    def get(self, i):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        # 1. Determine correct ArrayStack (ASS) half, and
        # 2. transform global index 'i' to local index 'p'
        stack_half, p = self._get_as_half_and_p(i)

        # 3. locate block index and get block from ArrayStack.
        b = self._i2b(p)
        block = stack_half.get(b)

        # 4. get local offset inside block using
        # local index 'p' on block index 'b'
        j = self._determine_block_offset(p, b)

        # 5. depending on array, get value from block,
        # if front: reversed order and mirrored offset.
        # if back : simple index.
        if stack_half == self.front:
            return block[len(block) - j - 1]
        else:
            return block[j]

    def set(self, i: int, x: Any):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        stack_half, p = self._get_as_half_and_p(i)

        b = self._i2b(p)
        block = stack_half.get(b)

        j = self._determine_block_offset(p, b)

        if stack_half == self.front:
            old = block[len(block) - j - 1]
            block[len(block) - j - 1] = x
        else:
            old = block[j]
            block[j] = x

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

    def _i2b(self, i: int):
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def _determine_block_offset(self, i: int, b: int):
        """
        If index i is in block b, then the number of
        elements in blocks 0, ... , b - 1 is b(b + 1)/2.
        Therefore, j, the offset of i,
        is stored at location:

        """
        return i - b * (b + 1) // 2

    def _get_as_half_and_p(self, i: int):
        """
        Returns correct ArrayStack half, and its local index.

        Translates similar to a DualArrayDeque, back to back.
        Makes use of the total number of elements stored
        in the front half (self.front_n).

        """
        if i < self.front_n:
            p = self.front_n - i - 1
            return self.front, p
        else:
            p = i - self.front_n
            return self.back, p

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
        """ """

        out = []
        out.append("\n=== Improved RootishArrayStack ===")
        out.append(f"elements           : {self.n}")
        # out.append(f"logical blocks     : {self.blocks.n}")
        # out.append(f"reserved blocks    : {len(self.blocks.a) - self.blocks.n}\n")

        return "\n".join(out)
