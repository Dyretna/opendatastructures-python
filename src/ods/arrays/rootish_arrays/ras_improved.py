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

    front_blocks (but reversed, back to back)

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
        self.back_n = 0
        self.front = ArrayStack()
        self.back = ArrayStack()

    @property
    def size(self):
        return self.n

    @property
    def total_blocks(self):
        return self.front.size + self.back.size

    def is_empty(self):
        return self.n == 0

    def get(self, i):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        # 1. Determine correct ArrayStack half, and
        # 2. transform global index 'i' to local index 'p'
        stack_half, p = self._get_as_half_and_p(i)

        # 3. locate block index and get block from ArrayStack.
        b = self._i2b(p)
        block = stack_half.get(b)

        # 4. get local offset inside block using
        # local index 'p' on block index 'b'
        j = self._determine_block_offset(p, b)

        return block[j]

    def set(self, i: int, x: Any):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        stack_half, p = self._get_as_half_and_p(i)
        b = self._i2b(p)
        block = stack_half.get(b)
        j = self._determine_block_offset(p, b)

        old = block[j]
        block[j] = x

        return old

    def add(self, i: int, x: Any):
        self._index_bounds_check_adding(i)

        # As in original RAS, element counters must
        # increment before shifting.
        self.n += 1
        if i < self.front_n or i <= 1:
            # ensure space in stack half, grow if needed
            self._maybe_grow(self.front, self.front_n)
            self.front_n += 1
            # front: already reversed, forward shifting
            for k in range(i):
                self.set(k, self.get(k + 1))
        else:
            self._maybe_grow(self.back, self.back_n)
            self.back_n += 1
            # back: normal backwards shifting
            for k in range(self.size - 1, i, -1):
                self.set(k, self.get(k - 1))

        self.set(i, x)
        self._balance()

    def remove(self, i: int) -> Any:
        if self.is_empty():
            raise IndexError("Stack is empty.")
        self._index_bounds_check(i)

        x = self.get(i)
        if i < self.front_n:
            for k in range(i, 0, -1):
                self.set(k, self.get(k - 1))

            self.set(0, None)
            self.front_n -= 1
            self._shrink(self.front, self.front_n)

        else:
            for k in range(i, self.size - 1):
                self.set(k, self.get(k + 1))

            self.set(self.size - 1, None)
            self.back_n -= 1
            self._shrink(self.back, self.back_n)

        self.n -= 1
        self._balance()

        return x

    # ---------------------------------------------------
    # internal helpers
    # ---------------------------------------------------

    def _index_bounds_check(self, i: int) -> None:
        if not (0 <= i <= self.size - 1):
            raise IndexError(f"index not in range: {i}")

    def _index_bounds_check_adding(self, i: int) -> None:
        if not (0 <= i <= self.size):
            raise IndexError(f"index not in range: {i}")

    def _i2b(self, i: int) -> int:
        return int(ceil((-3.0 + sqrt(9 + 8 * i)) / 2.0))

    def _determine_block_offset(self, i: int, b: int) -> int:
        """
        If index i is in block b, then the number of
        elements in blocks 0, ... , b - 1 is b(b + 1)/2.
        Therefore, j, the offset of i,
        is stored at location:

        """
        return i - b * (b + 1) // 2

    def _get_as_half_and_p(self, i: int) -> tuple[ArrayStack, int]:
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

    def _maybe_grow(self, ass: ArrayStack, count: int) -> None:
        # add a new block of size r+1 (filled with None)
        r = ass.size
        if r * (r + 1) / 2 < count + 1:
            new_block = [None] * (r + 1)
            # append at the end of blocks
            ass.add(ass.size, new_block)

    def _shrink(self, ass: ArrayStack, count: int) -> None:
        r = ass.size
        while r > 0 and ((r - 1) * (r - 2)) // 2 >= count:
            ass.a[r - 1] = None
            ass.remove(r - 1)
            r -= 1

    def _balance(self) -> None:
        """Balancing stacks element-wise."""
        if self.size <= 4:
            return

        if not (3 * self.front_n < self.back_n or 3 * self.back_n < self.front_n):
            return

        # snapshot
        data = self._contents()

        # reset structure
        self.front = ArrayStack()
        self.back = ArrayStack()

        self.front_n = self.size // 2
        self.back_n = self.size - self.front_n

        # rebuild front half (reversed)
        for i in range(self.front_n):
            self._append_to_half(self.front, data[self.front_n - i - 1], i)

        # rebuild back half (normal)
        for i in range(self.back_n):
            self._append_to_half(self.back, data[self.front_n + i], i)

    def _append_to_half(self, ass: ArrayStack, x: Any, count: int) -> None:
        r = ass.size

        if r * (r + 1) // 2 < count + 1:
            ass.add(r, [None] * (r + 1))

        b = self._i2b(count)
        j = self._determine_block_offset(count, b)

        ass.get(b)[j] = x

    def _contents(self):
        """Logical contents, front to back, via public API."""
        return [self.get(i) for i in range(self.size)]

    def __str__(self) -> str:
        out = []
        out.append(" Improved RootishArrayStack ".center(50, "="))
        out.append(f" Contents :  {self._contents()}")
        out.append(f" Front    :  {self.front.a}")
        out.append(f" back     :  {self.back.a}")

        out.append(
            f" BLOCKS   : {self.total_blocks}, "
            f" front: {self.front.size}, "
            f" back: {self.back.size}"
        )

        out.append(
            f" SIZE     : {self.size},  front: {self.front_n},  back: {self.back_n}"
        )

        out.append("=" * 50)

        return "\n" + "\n".join(out) + "\n"
