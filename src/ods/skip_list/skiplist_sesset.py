"""
SESSet (Exercise 4.13): elements live, in order, in the blocks of an
SEList-like structure, linked as a skiplist; space is O(n) for the
elements plus O(n/b + b) waste.

TODO-ish: add/remove/rebalance each descend the skiplist separately;
a finger search could reuse the neighbourhood found by the first
descent instead of restarting at the sentinel.
"""

import random
from typing import Optional

from ..arrays import BoundedDeque
from ..base import BaseSet


class Node:
    """
    A SESSet node stores a container (BDeque) to hold items,
    and an array of forward pointers. u.next[i] points to the
    sucessor of u in level list L_i.
    At initialization it only builds the container, items are
    added in the SESSet user class add(x) method.
    """

    def __init__(self, h: int, b: int):
        self.d = BoundedDeque(b)
        self.h = h
        self.next = [None] * (h + 1)

    @property
    def height(self):
        return self.h

    def __str__(self):
        next_nodes = [self.next[i].d.a for i in range(self.height + 1) if self.next[i]]

        out = [" SESSet Node ".center(50, "=")]
        out.append(f"deque  : {self.d.a} ")
        out.append(f"cap    : {self.d.capacity} ")
        out.append(f"height : {self.height}")
        out.append(f"next   : {next_nodes}")

        return "\n".join(out)


class SESSet(BaseSet):
    """Space-efficient skiplist with SSet interface"""

    def __init__(self, b: int = 3):
        self.b = b  # block size
        self._initialize()

    def find(self, x: int) -> Optional[int]:
        """Returns x if it exists, otherwise returns successor or None"""

        if self.sentinel.next[0] is None or x > self.tail.d[self.tail.d.size - 1]:
            return None

        u = self._find_pred_node(x)
        u = self._resolve_target(u, x)
        i = self._find_index(u.d, x)

        # if index overshoots, x does not exist,
        # and successor y lives in next block
        if i < u.d.size:
            return u.d[i]
        else:
            return u.next[0].d[0]

    def add(self, x: int | float) -> bool:
        """
        Insert x into the SESSet.
        Returns True if inserted, False if x already exists.

        """
        # set is empty or if x is biggest,
        # inserts x either in tail if not full, or into new block.
        if self.tail is None or x > self.tail.d.get(self.tail.d.size - 1):
            self._append_x(x)
            self.n += 1
            return True

        # find node and index, check for duplicate
        u = self._find_pred_node(x)
        u = self._resolve_target(u, x)
        i = self._find_index(u.d, x)
        if i < u.d.size and u.d[i] == x:
            return False

        # make room, and update node and index
        while u.d.size == u.d.capacity:
            self._make_room(u)
            u = self._resolve_target(u, x)
            i = self._find_index(u.d, x)

        u.d.add(i, x)

        self.n += 1
        return True

    def remove(self, x: int) -> bool:
        """
        Remove x from the skiplist.
        Return True if removed, False if not found.

        """
        if self.sentinel.next[0] is None:
            return False
        if (
            self.tail is None
            or self.tail.d.size == 0
            or x > self.tail.d[self.tail.d.size - 1]
        ):
            return False

        u = self._find_pred_node(x)
        u = self._resolve_target(u, x)
        i = self._find_index(u.d, x)

        # canonical not-found check: never read d[i] unconditionally
        if not (i < u.d.size and u.d[i] == x):
            return False

        u.d.remove(i)
        self.n -= 1

        # gather check: b consecutive blocks at exactly b - 1 => no surplus
        # anywhere in the window; merge them into b - 1 blocks
        w = u
        r = 0
        while r < self.b and w is not None and w.d.size == self.b - 1:
            w = w.next[0]
            r += 1
        if r == self.b:
            self._gather(u)

        # cascade the deficit rightwards until absorbed (or tail reached)
        while u.d.size < self.b - 1 and u.next[0] is not None:
            u.d.add_last(u.next[0].d.remove_first())
            u = u.next[0]

        # cascade can empty the tail block: unlink it
        if u.d.is_empty():
            self._unlink(u)

        return True

    # --------------------------------------
    # Additional Public Utilities
    # --------------------------------------

    def to_list(self):
        return list(self)

    def clear(self):
        self._initialize()

    def __contains__(self, x: int):
        return self.find(x) == x

    def __len__(self) -> int:
        return self.n

    def __iter__(self):
        for block in self._iter_deques():
            yield from block

    def __str__(self):
        out = []
        items = "\n\t " + "\n\t ".join([f"{a}" for a in self._iter_deques()])
        out.append(" SESSet ".center(50, "="))
        out.append(f"height : {self.h}")
        out.append(f"size   : {self.n}")
        out.append(f"b      : {self.b}")
        out.append(f"items  : {items}")

        return "\n".join(out)

    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _iter_deques(self):
        u = self.sentinel.next[0]
        while u is not None:
            yield u.d.to_list()
            u = u.next[0]

    def _initialize(self):
        self.sentinel = Node(0, self.b)
        self.h = 0
        self.n = 0
        self.tail = None

    def _new_node(self, h: int) -> Node:
        """Create new node with given height."""
        return Node(h, self.b)

    def _pick_height(self):
        """Simulate coin tosses to determine node height."""
        z = random.getrandbits(32)
        k = 0
        while z & 1:  # if number is odd, 'checks least sign bit'.
            k += 1
            z >>= 1  # shift right so that lsb = next bit
        return k

    def _find_pred_node(self, x: int) -> Node:
        """
        Return the predecessor of x at level 0: the last block whose
        greatest element is < x.

        """
        u = self.sentinel
        r = self.h
        already_checked = None

        while r >= 0:
            while u.next[r] is not None:
                # already failed on a higher level: skip re-comparison
                if u.next[r] is already_checked:
                    break

                nxt = u.next[r]
                if nxt.d.size == 0:  # transiently empty block:
                    break  # stop; target logic handles it

                # THE FLIP: compare against the block's MAX, so the walk
                # jumps over whole blocks whose range lies entirely < x.
                if nxt.d[nxt.d.size - 1] < x:
                    u = nxt
                else:
                    already_checked = nxt  # this block begins x's region
                    break

            r -= 1

        return u

    def _resolve_target(self, predecessor: Node, x: int) -> Node:
        if predecessor.next[0] is None:
            return predecessor

        if predecessor.next[0].d.is_empty():
            return predecessor

        if predecessor.d.is_empty() or x >= predecessor.next[0].d[0]:
            return predecessor.next[0]

        return predecessor

    def _find_index(self, d: BoundedDeque, x: int) -> int:
        """Return the index of x in non-empty deque d, or the insertion
        index for x if x is not present.

        """
        approx_mid = (d.get(0) + d.get(d.size - 1)) / 2
        if x < approx_mid:
            i = 0
            while i < d.size and d[i] < x:
                i += 1
            return i

        i = d.size - 1
        while i >= 0 and d[i] > x:
            i -= 1

        if i >= 0 and d[i] == x:
            return i

        return i + 1

    def _gather(self, u: Node) -> None:
        """Merge b consecutive blocks into b - 1 blocks."""

        w = u
        for _ in range(self.b - 1):
            donor = w.next[0]
            while w.d.size < self.b:
                w.d.add_last(donor.d.remove_first())
            w = w.next[0]

        # w is now the b-th gathered block: empty, remove from all levels
        self._unlink(w)

    def _unlink(self, w: Node) -> None:
        """Splice node w out of every level it participates in."""

        pred0 = self.sentinel
        r = min(self.h, w.height)
        while r >= 0:
            q = self.sentinel
            while q.next[r] is not None and q.next[r] is not w:
                q = q.next[r]
            if q.next[r] is w:
                q.next[r] = w.next[r]
            if r == 0:
                pred0 = q
            r -= 1

        if self.tail is w:
            self.tail = pred0 if pred0 is not self.sentinel else None

    def _spread(self, walked: list[Node]) -> Node:
        """Spread b consecutive full blocks over b + 1 blocks.

        Returns the new block.

        """
        successor = walked[-1].next[0]  # whatever currently follows the run
        stop_value = successor.d.get(0) if successor is not None else None

        # create the new block, and grow the sentinel if it is taller
        new_block = self._new_node(self._pick_height())
        while self.h < new_block.height:
            self.h += 1
            self.sentinel.next.append(None)

        # one descending search, exactly like SkiplistSSet.add:
        # record the predecessor to the stack on every level, stopping at
        # the run's boundary (stop_value) on each level
        stack = [self.sentinel] * (self.h + 1)
        u = self.sentinel
        r = self.h
        while r >= 0:
            while u.next[r] is not None and (
                stop_value is None or u.next[r].d.to_list()[0] < stop_value
            ):
                u = u.next[r]
            stack[r] = u
            r -= 1

        # splice new_block into every chain from the stack
        for r in range(new_block.height + 1):
            new_block.next[r] = stack[r].next[r]
            stack[r].next[r] = new_block

        # maintain the tail invariant if the run ended at the tail
        if successor is None:
            self.tail = new_block

        # redistribute right-to-left over walked + [new_block]:
        blocks = walked + [new_block]
        for i in range(len(blocks) - 1, 0, -1):
            while blocks[i].d.size < self.b:
                blocks[i].d.add_first(blocks[i - 1].d.remove_last())

        return new_block

    def _append_block(self) -> Node:
        """Create a new block node and append it at the tail of all levels."""
        w = self._new_node(self._pick_height())

        # grow level structure if needed (also extends sentinel.next)
        while self.h < w.height:
            self.h += 1
            self.sentinel.next.append(None)

        # level 0: the cache gives us the predecessor directly
        if self.tail is None:
            self.sentinel.next[0] = w  # empty list: sentinel precedes
        else:
            self.tail.next[0] = w

        # levels 1..height: find the last node on each level
        # only where links actually exist
        for r in range(1, w.height + 1):
            u = self.sentinel
            while u.next[r] is not None:
                u = u.next[r]
            u.next[r] = w

        self.tail = w
        return w

    def _append_x(self, x: int | float):
        """Inserts x either in tail if not full, or into new block."""
        if self.tail is not None and not self.tail.d.is_full():
            self.tail.d.add(self.tail.d.size, x)
        else:
            w = self._append_block()
            w.d.add(0, x)

    def _make_room(self, u: Node) -> None:
        """Create one free slot in u. Direct port of SEList.add() logic"""
        walked = []
        w = u
        r = 0

        while r < self.b and w is not None and w.d.is_full():
            walked.append(w)
            w = w.next[0]
            r += 1

        if r == self.b:
            self._spread(walked)
            return

        if w is None:  # ran off the end: the run is shorter than b
            w = self._append_block()

        # redistribute right-to-left over walked
        for i in range(len(walked) - 1, -1, -1):
            w.d.add_first(walked[i].d.remove_last())
            w = walked[i]
