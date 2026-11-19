import random
from typing import Optional

from ..base import BaseSet


class Node:
    """
    A skiplist node stores a value x and an array of forward pointers.
    u.next[i] points to the sucessor of u in level list L_i.
    """

    def __init__(self, x: Optional[int], h: int):
        self.x = x
        self.h = h
        self.next = [None] * (h + 1)

    @property
    def height(self):
        return self.h

    def __str__(self):
        next_nodes = [
            str(self.next[i].x) for i in range(self.height + 1) if self.next[i]
        ]

        out = [" SkiplistSSet Node ".center(50, "=")]
        out.append(f"x      : {self.x} ")
        out.append(f"height : {self.height}")
        out.append(f"next   : {next_nodes}")

        return "\n".join(out)


class SkiplistWithFinger(BaseSet):
    """
    A probabilistic Sorted Set implementation based on a skiplist.

    Elements are stored in sorted order and support expected
    O(log n) search, insertion, and removal operations.

    This subclass stores a finger, which is then used so that every
    find(x) operation is implemented as a finger search. During each
    find(x) operation the finger is updated so that each find(x)
    operation uses, as a starting point, a finger that points to the
    result of the previous find(x) operation.

    It is possible to prove that the expected number of steps required
    for a finger search is O(1 + log r), where r is the number values
    in L0 between x and the value pointed to by the finger.

    """

    def __init__(self):
        self.sentinel = Node(None, 0)
        self.h = 0
        self.n = 0
        self.finger: list[Node] = [self.sentinel]

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
        while self.h < w.height:
            self.h += 1
            self.sentinel.next.append(None)
            stack.append(self.sentinel)

        # 4. Splice w into the lists (why we need stack)
        for i in range(len(w.next)):
            w.next[i] = stack[i].next[i]  # w points gets old predecessor pointer
            stack[i].next[i] = w  # predecessor now points to w

        # 5. reset the finger - splice changed the search space
        self.finger = [self.sentinel]

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
            # 5. reset the finger - node pointers may be gone
            self.finger = [self.sentinel]

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
        out = []
        out.append(" SkiplistSSet ".center(50, "="))
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

    def _key(self, node: "Node"):
        """sort key for a finger entry; the sentinel acts as -infinity"""
        return node.x if node is not self.sentinel else float("-inf")

    def _find_pred_node(self, x: int):
        """
        Return the predecessor of x (largest value < x) at level 0.

        Finger search: climb the stored finger until reaching a node u
        with u.x < x (and u.next is None or u.next.x > x), then perform
        a normal search for x starting from (u, r).

        """
        # 0. keep finger array in sync with current height
        #    (length must always be self.h + 1, entries: node or sentinel)
        if len(self.finger) < self.h + 1:
            self.finger.extend([self.sentinel] * (self.h + 1 - len(self.finger)))

        # 1. climb the finger. On the very first call every entry is the
        #    sentinel (key = -inf < x), so we climb to the top and get
        #    a normal full search -- no special case needed.
        if self._key(self.finger[0]) < x:  # forwards, x to the right
            r = 0
            while (
                r + 1 < len(self.finger)
                and self.finger[r].next[r] is not None
                and self.finger[r].next[r].x < x
            ):
                r += 1
        else:  # backwards, x to the left
            r = 0
            while (
                r < len(self.finger)
                and self.finger[r] is not self.sentinel
                and self.finger[r].x >= x
            ):
                r += 1

        # 2. decide the starting point (u, r) for the downwards search
        if (
            r == len(self.finger)  # climbed past array
            or self.finger[r] is self.sentinel  # hit the sentinel
            or self.finger[r].x >= x
        ):  # entry is not a predecessor
            u, r = self.sentinel, self.h
        else:
            u = self.finger[r]

        # 3. normal traversal downwards, saving the new finger
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

            self.finger[r] = u
            r -= 1

        return self.finger[0]
