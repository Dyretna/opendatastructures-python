import random
from typing import Optional

from ..base import BaseSet
from ..validation import Validator as Val


class Node:
    """
    A skiplist node stores a value x and an array of forward pointers.
    u.next[i] points to the sucessor of u in level list L_i.
    """

    def __init__(self, x: Optional[int], h: int):
        self.x = x
        self.length: list[int] = [0] * (h + 1)
        self.next: list[Optional[Node]] = [None] * (h + 1)

    @property
    def height(self):
        return len(self.next) - 1

    def __str__(self):
        next_nodes = [
            str(self.next[i].x) for i in range(self.height + 1) if self.next[i]
        ]

        out = [" SkiplistSSet Node ".center(50, "=")]
        out.append(f"x      : {self.x} ")
        out.append(f"height : {self.height}")
        out.append(f"next   : {next_nodes}")

        return "\n".join(out)


class SkiplistWithRank(BaseSet):
    """
    A SkiplistSSet version that implements fast access to
    elements in O(log n) time with a get(i) method.

    We make use of methods developed in the SkiplistList variant:
    - Node with the height property to store distance
    when traversing right.
    - method to find predecessor node by rank / index

    and beyond that, add additional book-keeping add(x)
    and remove(x) methods.

    """

    def __init__(self):
        self.sentinel = Node(None, 0)
        self.h = 0
        self.n = 0

    # --------------------------------------
    # Public Interface
    # --------------------------------------

    @property
    def size(self):
        return self.n

    def get(self, i: int):
        Val.validate_index_access(i, self.size)
        return self._find_pred_by_rank(i).next[0].x

    def find(self, x: int) -> Optional[int]:
        """Returns x if it exists, otherwise None"""

        u = self._find_pred_by_value(x)
        if u.next[0] is None:
            return None
        return u.next[0].x

    def add(self, x: int) -> bool:
        """Insert x inte the skiplist.

        Returns True if inserted, False if already exists

        """
        stack: list[Optional[Node]] = [None] * (self.h + 1)
        js = [0] * (self.h + 1)  # js[r] index of stack[r] (j per level)
        u = self.sentinel
        r = self.h
        j = -1  # index of u, shared across levels

        # 1. Value-based descent: preds + their indices
        while r >= 0:
            # Go right without overshooting x
            while u.next[r] is not None and u.next[r].x < x:
                j += u.length[r]
                u = u.next[r]

            # check for duplicate (SSet specific)
            if u.next[r] is not None and u.next[r].x == x:
                return False

            stack[r] = u
            js[r] = j
            r -= 1

        # 2. New Node + grow sentinel (both arrays!)
        w = self._new_node(x, self._pick_height())
        while self.h < w.height:
            self.h += 1
            self.sentinel.next.append(None)
            stack.append(self.sentinel)
            self.sentinel.length.append(self.n + 1)
            js.append(-1)

        # 3. Insertion index: level-0 pred's index + 1
        i = js[0] + 1

        # 4. Splice + booking-keeping (Morin's formulas, split in two phases)
        for r in range(w.height + 1):
            u: Node = stack[r]
            w.next[r] = u.next[r]
            u.next[r] = w
            w.length[r] = u.length[r] + 1 - (i - js[r])
            u.length[r] = i - js[r]

        # Edges above w now span one more
        for r in range(w.height + 1, self.h + 1):
            stack[r].length[r] += 1

        self.n += 1
        return True

    def remove(self, x: int) -> bool:
        """
        Remove x from the skiplist.
        Return True if removed, False if not not found.

        """
        # SSet specific: x may not exist
        pred = self._find_pred_by_value(x)
        if pred.next[0] is None or pred.next[0].x != x:
            return False

        u = self.sentinel
        r = self.h
        j = -1

        while r >= 0:
            # Go right without overshooting x
            while u.next[r] is not None and u.next[r].x < x:
                j += u.length[r]
                u = u.next[r]

            u.length[r] -= 1  # Node ahead disappears

            # check for duplicate
            if u.next[r] is not None and u.next[r].x == x:
                u.length[r] += u.next[r].length[r]  # absorb its span
                u.next[r] = u.next[r].next[r]
                if u == self.sentinel and u.next[r] is None:
                    self.h -= 1
            r -= 1

        self.n -= 1
        return True

    # --------------------------------------
    # Additional Public Utilities
    # --------------------------------------

    def to_list(self) -> list[int]:
        """Convert to sorted list (for debugging / testing)."""
        result = []
        u = self.sentinel.next[0]
        while u is not None:
            result.append(u.x)
            u = u.next[0]
        return result

    def __contains__(self, x: int):
        return self.find(x) == x

    def __len__(self) -> int:
        return self.n

    def __str__(self):
        out = []
        out.append(" SkiplistSSetWithGet ".center(50, "="))
        out.append(f"items  : {self.to_list()}")
        out.append(f"height : {self.h}")
        out.append(f"size   : {self.n}")

        return "\n".join(out)

    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _new_node(self, x: int, h: int) -> Node:
        """Create new node with given height."""
        return Node(x, h)

    def _pick_height(self):
        """Simulate coin tosses to determine node height."""
        z = random.getrandbits(32)
        k = 0
        while z & 1:  # if number is odd, 'checks least sign bit'.
            k += 1
            z >>= 1  # shift right so that lsb = next bit
        return k

    def _find_pred_by_value(self, x: int):
        """
        Return the predecessor of x (largest value < x) at level 0.
        Exercise 4.8: avoids redundant comparisons.
        """
        u = self.sentinel
        r = self.h
        already_checked = None

        while r >= 0:
            while u.next[r] is not None:
                # we already know this node failed the comparison
                # on a higher level, so skip comparison
                if u.next[r] is already_checked:
                    break

                if u.next[r].x < x:
                    u = u.next[r]
                else:
                    already_checked = u.next[r]
                    break

            r -= 1

        return u

    def _find_pred_by_rank(self, i: int):
        """
        Return the predecessor of i at level 0.
        """
        u = self.sentinel
        r = self.h
        j = -1

        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j = j + u.length[r]
                u = u.next[r]  # go right in list r
            r -= 1  # go down into list r-1
        return u
