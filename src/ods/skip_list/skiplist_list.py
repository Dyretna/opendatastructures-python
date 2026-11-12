import random
from typing import Optional

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


class SkiplistList:
    """
    A SkiplistList implements the List interface using a skiplist
    structure. In a SkiplistList, L0 contains the elements of the
    list in the order in which they appear in the list. As in a
    SkiplistSSet, elements can be added, removed, and accessed
    in O(log n) time.

    """

    def __init__(self):
        self.sentinel = Node(None, 0)
        self.h = 0
        self.n = 0

    # --------------------------------------
    # Morrins Interface
    # --------------------------------------

    @property
    def size(self):
        return self.n

    def get(self, i: int):
        Val.validate_index_access(i, self.size)
        return self._find_pred(i).next[0].x

    def set(self, i: int, x: int):
        Val.validate_index_access(i, self.size)
        u = self._find_pred(i).next[0]
        y = u.x
        u.x = x
        return y

    def add(self, i: int, x: int) -> bool:
        """Insert x at index i the skiplist."""
        Val.validate_index_insert(i, self.size)
        w = self._new_node(x, self._pick_height())

        if w.height > self.h:
            self.h += 1
            self.sentinel.next.append(None)
            self.sentinel.length.append(self.n + 1)

        self._add(i, w)

    def _add(self, i: int, w: Node) -> Node:
        u = self.sentinel
        k = w.height
        r = self.h
        j = -1  # index for u (sentinel = -1)

        # while traversing from top to bottom:
        while r >= 0:
            # same traversal as in _find_pred()
            while u.next[r] is not None and j + u.length[r] < i:
                j += u.length[r]  # jump u index by length
                u = u.next[r]

            # everything after insertion shifts + 1
            u.length[r] += 1

            # === SPLICE AT LEVELS THE NEW NODES REACHES (r <= k) ===
            # w only participates in levels 0..k (w height), so only there
            # do we connect u -> w -> z (old successor)
            if r <= k:
                w.next[r] = u.next[r]  # w inherits u's successor
                u.next[r] = w
                w.length[r] = u.length[r] - (i - j)  # w keeps the tail of u's old span
                u.length[r] = i - j  # u ends at the insertion point

            r -= 1  # travel down one level

        self.n += 1

        return u

    def remove(self, i: int) -> bool:
        """Remove from index i and return x from the skiplist."""
        Val.validate_index_access(i, self.size)
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
                u.length[r] += u.next[r].length[r]  # absorb its span
                u.next[r] = u.next[r].next[r]
                if u == self.sentinel and u.next[r] is None:
                    self.h -= 1
            r -= 1

        self.n -= 1

        return x

    # --------------------------------------
    # Additional Public Utilities
    # --------------------------------------

    def absorb(self, skiplist: "SkiplistList") -> None:
        pass

    def truncate(self, i: int) -> "SkiplistList":
        """
        Remove and return the tail of the list at index i.

        After Execution, self holds only the elements at indices
        0, ...., i-1, and the returned SkiplistList holds the
        elements at indices i, ..., n-1.

        Works like _find_pred(): descend from top level, moving
        right while tracking j, the index of u (sentinel = -1).
        On every level where u.next[r] connects past index i,
        that connection hands over the whole rest of level r to
        the new tail sentinel, so each level is visited once.

        Runs in O(log n) expected time.

        """
        Val.validate_index_insert(i, self.size)  # i == n is lega: empty

        # New sentinel for the tail list: give it full height for now,
        # so it can recive pointers at every level. Trims below.
        tail = SkiplistList()
        tail.sentinel = Node(None, self.h)
        tail.n = self.n - i

        u = self.sentinel
        r = self.h
        j = -1  # index for u (sentinel = -1)
        tail_h = 0  # height of the tail list: (highest cut level) + 1

        # Descend from top level to bottom, cutting links behind us.
        while r >= 0:
            # same traversal as in _find_pred()
            while u.next[r] is not None and j + u.length[r] < i:
                j = j + u.length[r]  # jump u index by length
                u = u.next[r]

            # if u.next[r] exists here, its index is >= i, so it belongs
            # to the tail: hand over the rest of level r to the tail
            # sentinel, then cut the link on self's side.
            if u.next[r] is not None:
                k = j + u.length[r]  # old index of u.next[r]
                tail.sentinel.next[r] = u.next[r]  # tail inherits link
                tail.sentinel.length[r] = k - i + 1  # sentinel-offset

                u.next[r] = None  # cut
                u.length[r] = i - 1 - j  # elements remaining in list
                tail_h = max(tail_h, r)

            r -= 1  # travel down one level

        # --- Set sizes and heights ---
        self.n = i
        tail.h = tail_h

        # trim the tail sentinel down to the height it actually uses.
        while len(tail.sentinel.next) - 1 > tail_h:
            tail.sentinel.next.pop()
            tail.sentinel.length.pop()
        # Drop now-empty top levels of self
        while self.h > 0 and self.sentinel.next[self.h] is None:
            self.h -= 1

        return tail

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
