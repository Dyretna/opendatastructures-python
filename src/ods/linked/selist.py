from typing import Any, Optional

from ..arrays import BoundedDeque
from ..base import BaseList
from ..validation import Validator as Val


class Node:
    def __init__(self, b: int):
        self.d = BoundedDeque(b)  # BDeque holds up to b+1 elements
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class SEList(BaseList):
    """

    Theorem
    -------
    An SEList implements the List interface. Ignoring the cost
    of calls to spread(u) and gather(u), an SEList with block size b
    supports the operations

    - get(i) and set(i, x) in O(1 + min{i, n - i}/b) time per operation; and
    - add(i, x) and remove(i) in O(b + min{i, n - i}/b) time per operation.

    Furthermore, beginning with an empty SEList, any sequence of m
    add(i, x) and remove(i) operations results in a total of O(bm)
    time spent during all calls to spread(u) and gather(u).

    The space (measured in words) used by an SEList that stores n
    elements is n + O(b + n/b).

    """

    def __init__(self, block_size: int = 3):
        super(SEList, self).__init__()
        self.b = block_size  # blocks hold b+1 elements
        self._initialize()

    def get(self, i: int):
        Val.validate_index_access(i, self.size)
        u, j = self._get_location(i)
        return u.d.get(j)

    def set(self, i: int, x: Any):
        Val.validate_index_access(i, self.size)
        u, j = self._get_location(i)
        return u.d.set(j, x)

    def add(self, i: int, x: Any):
        Val.validate_index_insert(i, self.size)
        # if we add to end - simply append
        if i == self.n:
            self.append(x)
            return

        u, j = self._get_location(i)
        r = 0  # number of steps
        w = u
        # --------------------------------------------------------------
        # count how many consecutive nodes starting at u are full (b+1)
        # stop early if we hit the dummy (list ended) or an under-full node
        # --------------------------------------------------------------
        while r < self.b and w is not self.dummy and w.d.size == self.b + 1:
            w = w.next
            r += 1
        # --------------------------------------------------------------
        # if more steps than size of blocks we have to add a new node,
        # and spread elements to make space
        # --------------------------------------------------------------
        if r == self.b:  # b blocks, each with b+1 elements
            self._spread(u)
            w = u

        if w == self.dummy:  # ran off the end - add new node
            w = self._add_before(w)

        while w is not u:  # work backwards, shifting as we go
            w.d.add_first(w.prev.d.remove_last())
            w = w.prev

        w.d.add(j, x)
        self.n += 1

    def append(self, x: Any):
        last = self.dummy.prev
        if last == self.dummy or last.d.size == self.b + 1:
            last = self._add_before(self.dummy)
        last.d.append(x)
        self.n += 1

    def remove(self, i: int):
        if self.n == 0:
            raise IndexError("List is empty")
        Val.validate_index_access(i, self.size)

        u, j = self._get_location(i)
        y = u.d.get(j)
        w = u
        r = 0

        while r < self.b and w is not self.dummy and w.d.size == self.b - 1:
            w = w.next
            r += 1
        # ---------------------------------------------------------
        # 1. if b following nodes ar too empty (b-1)
        # 2. compress via gather
        # 3. remove the element j in node u,
        # 4. fill gaps shift from right until u has at least b-1,
        # 5. delete node if empty.
        # ---------------------------------------------------------
        if r == self.b:  # b blocks, each with b - 1 elements
            self._gather(u)
        u.d.remove(j)

        while u.d.size < (self.b - 1) and u.next is not self.dummy:
            u.d.add_last(u.next.d.remove_first())
            u = u.next

        if u.d.size == 0:
            self._remove_node(u)

        self.n -= 1
        return y

    def clear(self):
        self._initialize()

    def __iter__(self):
        u = self.dummy.next
        while u is not self.dummy:
            for x in u.d:
                yield x
            u = u.next

    def __str__(self):
        out = []
        out.append(" Space Efficient Linked List ".center(50, "="))
        out.append(f"n : {self.n}")

        u = self.dummy.next
        while u != self.dummy:
            block = []
            for raw_idx in range(u.d.n):
                block.append(u.d.get(raw_idx))
            empty_slots = [None] * (u.d.capacity - u.d.n)
            out.append("node: " + str(block + empty_slots))
            u = u.next

        return "\n".join(out)

    # --------------------------------------
    # Internal Helpers
    # --------------------------------------

    def _initialize(self):
        self.dummy = self._new_node()
        self.dummy.next = self.dummy.prev = self.dummy
        self.n = 0

    def _get_location(self, i: int) -> tuple[Node, int]:
        """Returns correct Node and block index."""
        # Walk from whichever end of the list is closer
        # to i, stepping over whole blocks. Each block's
        # size is subtracted from the target index until
        # it falls inside the current block.

        if i < self.size // 2:
            # Closer to the front: walk forward from the
            # first block. Invariant: i is now an offset
            # relative to the start of u.
            u = self.dummy.next
            while i >= u.d.size:
                i -= u.d.size
                u = u.next
            return u, i
        # Closer to the back: walk backward from the
        # dummy. Invariant: idx is the number of elements
        # before u (i.e. i counts elements from the end of
        # u's block onwards).
        else:
            u = self.dummy
            idx = self.n
            while i < idx:
                u = u.prev
                idx -= u.d.size
        return u, i - idx

    def _new_node(self) -> Node:
        return Node(self.b)

    def _remove_node(self, w: Node):
        w.prev.next = w.next
        w.next.prev = w.prev

    def _add_before(self, w: Node) -> Node:
        u = self._new_node()
        u.prev = w.prev
        u.next = w
        u.next.prev = u
        u.prev.next = u
        return u

    def _spread(self, u: Node) -> None:
        w = u
        for _ in range(self.b):
            w = w.next

        w = self._add_before(w)
        while w is not u:
            while w.d.size < self.b:
                w.d.add_first(w.prev.d.remove_last())
            w = w.prev

    def _gather(self, u: Node) -> None:
        w = u
        for _ in range(self.b - 1):
            while w.d.size < self.b:
                w.d.add_last(w.next.d.remove_first())
            w = w.next
        self._remove_node(w)
