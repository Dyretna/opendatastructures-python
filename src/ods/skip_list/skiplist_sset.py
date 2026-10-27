import random
from typing import Optional


class Node:
    """
    A skiplist node stores a value x and an array of forward pointers.
    u.next[i] points to the sucessor of u in level list L_i.
    """

    def __init__(self, x: Optional[int], h: int):
        self.x = x
        self.h = h
        self.next = [None] * (h + 1)

    def height(self):
        return self.h


class SkiplistSSet:
    """
    A probabilistic Sorted Set implementation based on a skiplist.

    Elements are stored in sorted order and support expected
    O(log n) search, insertion, and removal operations.

    Conceptually, a skiplist consists of multiple linked levels
    stacked on top of each other. In practice, this implementation
    stores each element only once. Every node maintains an array
    of forward pointers, where next[r] represents the node's
    successor on level r.

    Node heights are chosen randomly, causing some nodes to appear
    on multiple levels and act as shortcuts during searches.

    """

    def __init__(self):
        self.sentinel = Node(None, 0)
        self.h = 0
        self.n = 0

    # --------------------------------------
    # Morrins Interface
    # --------------------------------------

    def find(self, x: int) -> Optional[int]:
        """Returns x if it exists, otherwise None"""

        u = self._find_pred_node(x)
        if u.next[0] is None:
            return None
        return u.next[0].x

    def add(self, x: int) -> bool:
        """Insert x inte the skiplist.

        Returns True if inserted, False if already exists

        """
        stack = [None] * (self.h + 1)
        u = self.sentinel
        r = self.h

        # 1. find predecessors at each level and store
        # them in stack.
        while r >= 0:
            # Go right without overshooting x
            while u.next[r] is not None and u.next[r].x < x:
                u = u.next[r]

            # check for duplicate
            if u.next[r] is not None and u.next[r].x == x:
                return False

            # record that u is the predecessor at level r
            stack[r] = u
            r -= 1

        # 2. Create a new Node with random height
        w = self._new_node(x, self._pick_height())

        # 3. If new node is taller than current, extend stack
        while self.h < w.height():
            self.h += 1
            self.sentinel.next.append(None)
            stack.append(self.sentinel)

        # 4. Splice w into the lists (why we need stack)
        for i in range(len(w.next)):
            w.next[i] = stack[i].next[i]  # w points gets old predecessor pointer
            stack[i].next[i] = w  # predecessor now points to w

        self.n += 1
        return True

    def remove(self, x: int) -> bool:
        """
        Remove x from the skiplist.
        Return True if removed, False if not not found.

        """
        removed = False
        u = self.sentinel
        r = self.h

        while r >= 0:
            # Go right without overshooting x
            while u.next[r] is not None and u.next[r].x < x:
                u = u.next[r]

            # check for duplicate
            if u.next[r] is not None and u.next[r].x == x:
                removed = True
                u.next[r] = u.next[r].next[r]
                if u == self.sentinel and u.next[r] is None:
                    self.h -= 1  # height has decreased
            r -= 1

        if removed:
            self.n -= 1

        return removed

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
        pass

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

    def _find_pred_node(self, x: int):
        """
        Return the predecessor of x (largest value < x) at level 0.
        """
        u = self.sentinel
        r = self.h

        while r >= 0:
            while u.next[r] is not None and u.next[r].x < x:
                u = u.next[r]  # go right in list r
            r -= 1  # go down into list r-1
        return u
