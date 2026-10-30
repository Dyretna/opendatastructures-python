import random
from typing import Optional


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


class SkiplistList:
    """ """

    def __init__(self):
        self.sentinel = Node(None, 0)
        self.h = 0
        self.n = 0

    # --------------------------------------
    # Morrins Interface
    # --------------------------------------

    def get(self, i: int):
        return self._find_pred(i).next[0].x

    def set(self, i: int, x: int):
        u = self._find_pred(i).next[0]
        y = u.x
        u.x = x
        return y

    def add(self, i: int, x: int) -> bool:
        """Insert x at index i the skiplist."""
        w = self._new_node(x, self._pick_height())

        if w.height > self.h:
            self.h += 1
            self.sentinel.next.append(None)
            self.sentinel.length.append(self.n + 1)

        print("h =", self.h)
        print("sentinel next =", len(self.sentinel.next))
        print("sentinel length =", len(self.sentinel.length))
        print("new node height =", w.height)

        self._add(i, w)

    def _add(self, i: int, w: Node):
        u = self.sentinel
        k = w.height
        r = self.h
        j = -1

        while r >= 0:
            print("r =", r, "len(u.next) =", len(u.next), "node =", u.x)

            while u.next[r] is not None and j + u.length[r] < i:
                j = j + u.length[r]
                u = u.next[r]

            u.length[r] = u.length[r] + 1
            if r <= k:
                w.next[r] = u.next[r]
                u.next[r] = w
                w.length[r] = u.length[r] - (i - j)
                u.length[r] = i - j

            r -= 1

        self.n += 1

        return u

    def remove(self, i: int) -> bool:
        """Remove from index i and return x from the skiplist."""
        u = self.sentinel
        r = self.h
        j = -1

        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j = j + u.length[r]
                u = u.next[r]

            u.length[r] = u.length[r] - 1
            if j + u.length[r] + 1 == i and u.next[r] is not None:
                x = u.next[r].x
                u.length[r] = u.length[r] + u.next[r].length[r]
                u.next[r] = u.next[r].next[r]
                if u == self.sentinel and u.next[r] is None:
                    self.h -= 1
            r -= 1

        self.n -= 1

        return x

    # --------------------------------------
    # Additional Public Utilities
    # --------------------------------------

    def to_list(self) -> list[int]:
        """Convert to list (for debugging / testing)."""
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
        out.append(" SkiplistList ".center(50, "="))
        out.append(f"items  : {self.to_list()}")
        out.append(f"height : {self.h}")
        out.append(f"length : {self.n}")

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

    def _find_pred(self, i: int):
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
