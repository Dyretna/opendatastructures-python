from math import ceil
from typing import Any

from .array_deques import ArrayDeque


class TreQueue:
    def __init__(self):
        self.left  = ArrayDeque()
        self.mid   = ArrayDeque()
        self.right = ArrayDeque()

    def set(self, i:int, x:Any) -> None:
        block, idx = self._get_block_and_idx(i)
        block.set(idx, x)

    def get(self, i:int) -> Any:
        block, idx = self._get_block_and_idx(i)
        return block.get(idx)

    def add(self, i:int, x:Any) -> None:
        block, idx = self._get_block_and_idx(i, adding=True)
        block.add(idx, x)
        if self._needs_balance():
            self.balance()

    def remove(self, i:int) -> Any:
        block, idx = self._get_block_and_idx(i)
        x = block.remove(idx)
        if self._needs_balance():
            self.balance()
        return x

    def balance(self):
        """
        Balances the deques if _needs_balance() has passed,
        which ensures amortized O(1) time.

        As is hinted at by Morin, if we would simply
        initialize new ArrayDeques and use .add(i, x)
        that would cause a lot of calls to resize().

        Therefore, by initializing temporary lists,
        and storing elements with .get(i) while iterating,
        then using add_all() on new deques, only one call
        to resize() is needed.
        """
        n = self.left.n + self.mid.n + self.right.n
        third = ceil(n * 0.33)

        temp1 = [None] * third
        temp2 = [None] * third
        temp3 = [None] * (n - third * 2)

        for i in range(n):
            if i < third:
                temp1[i] = self.get(i)
            elif i < third*2:
                temp2[i-third] = self.get(i)
            else:
                temp3[i-third*2] = self.get(i)

        self.left = ArrayDeque()
        self.mid = ArrayDeque()
        self.right = ArrayDeque()

        self.left.add_all(0, temp1)
        self.mid.add_all(0, temp2)
        self.right.add_all(0, temp3)


    def rotate_left(self, r):
        pass

    def rotate_right(self, r):
        pass


    # --------------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------------

    def _get_block_and_idx(self, i, adding:bool = False):

        self._validate_i(i, adding=adding)
        if not all([self.left.n, self.mid.n, self.right.n]):
            if not self.left.n:
                return self.left, i
            elif not self.mid.n:
                return self.mid, i
            else:
                return self.right, i

        if i <= self.left.n - 1:
            return self.left, i
        elif i <= self.left.n + self.mid.n - 1:
            return self.mid,  i - self.left.n
        else:
            return self.right, i - (self.left.n + self.mid.n)

    def _validate_i(self, i:int, adding:bool = False):
        i_end = (self.left.n + self.mid.n + self.right.n) - 1
        if adding:
            i_end += 1
        if i_end < 0:
            raise ValueError("Container has no values!")
        if not 0 <= i <= i_end:
            raise IndexError(f"Index must be in range: 0 - {i_end}, got {i}")

    def _needs_balance(self) -> bool:
        """
        Decides WHEN balancing should occur.

        Triggers rebalancing when one segment
        grows to large relative to others.
            biggest >= 3 * smallest

        This threshold follows Morin's lazy-check pattern.
        It ensures amortized 0(1) per add/remove by limiting
        rebalance frequency.
        """
        biggest = max([self.left.n, self.mid.n, self.right.n])
        smallest = min([self.left.n, self.mid.n, self.right.n])
        return biggest >= max([3, smallest * 3])

    def _get_ordered_collection(self):
        # just a helper to get an ordered 'pretty print' for debugging
        ordered_c = []
        for block in [self.left, self.mid, self.right]:
            for k in range(block.n):
                ordered_c.extend(block.a[(block.j + k) % len(block.a)])

        return ordered_c

    def __lshift__(self, r):
        self.rotate_left(r)

    def __rshift__(self, r):
        self.rotate_right(r)

    def __str__(self):
        arr_strings = [self.left.__str__(), self.mid.__str__(), self.right.__str__()]
        return f"Ordered: {self._get_ordered_collection()}\n" + \
                "Deques:\n" + "\n".join(arr_strings)
